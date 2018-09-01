
import logging
import os
import re
import subprocess
import sys
import threading
import time

import yaml

from . import db_wrapper
from . import feh_runner
from . import x_wrapper

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)
RUNNING = True


def image_finder(db_filename, configuration):
    global RUNNING

    db = db_wrapper.DbWrapper(db_filename)
    _logger.info(
        "Scanning {} for images every 5 seconds".format(configuration["mountpoints"])
    )
    while RUNNING:
        images = []
        for mountpoint in configuration["mountpoints"]:
            if os.path.exists(mountpoint):
                _logger.debug("Scanning {}".format(mountpoint))
                for root, dirs, files in os.walk(mountpoint):
                    for filename in (os.path.join(root, f) for f in files):
                        _, ext = os.path.splitext(filename)
                        if ext.lower()[1:] in configuration["extensions"]:
                            _logger.debug("Adding image {}".format(filename))
                            images.append(filename)
        try:
            db.add_images(*tuple(images))
        except:
            RUNNING = False
        time.sleep(5)


def mounter():
    global RUNNING

    usb_pattern = re.compile(r"sd[a-z]\d+")

    _logger.info("Scanning /dev for USB devices")

    mounted = []
    while RUNNING:
        for entry in os.scandir("/dev/"):
            if usb_pattern.match(entry.name) and not os.path.exists(
                "/media/{}".format(entry.name)
            ):
                _logger.info("Mounting {}".format(entry.name))
                completed = subprocess.run(["pmount", "-r", entry.name], stderr=subprocess.PIPE)
                if completed.returncode != 0:
                    _logger.error(
                        "Failed to mount {}: ".format(entry.name, completed.stderr)
                    )
                else:
                    mounted.append(entry.name)
        time.sleep(1)

    for dev in mounted:
        _logger.info("Unmounting {}".format(dev))
        completed = subprocess.run(["pumount", dev], stderr=subprocess.PIPE)
        if completed.returncode != 0:
            _logger.error(
                "Failed to umount {}: ".format(entry.name, completed.stderr)
            )


def main():
    global RUNNING

    config_directory = os.path.join(os.path.dirname(__file__), "config")

    db_filename = "/tmp/piframe.db"
    init_script_filename = os.path.join(config_directory, "piframe.sql")
    config_filename = os.path.join(config_directory, "config.yaml")

    _logger.debug("Reading configuration from {}".format(config_filename))
    with open(config_filename) as config_file:
        configuration = yaml.safe_load(config_file)

    _logger.debug("Configuration:\n{}".format(configuration))

    feh = feh_runner.FehRunner(configuration.get("feh_options", []))
    if configuration.get("start_x", True):
        xserver = x_wrapper.XServer()
        xserver.start()

    image_finder_thread = threading.Thread(
        target=image_finder, args=(db_filename, configuration)
    )
    image_finder_thread.daemon = True
    image_finder_thread.start()

    usb_mounter_thread = None
    if configuration.get("automount", True):
        usb_mounter_thread = threading.Thread(target=mounter, args=())
        usb_mounter_thread.start()

    db = db_wrapper.DbWrapper(db_filename, init_script_filename)
    try:
        _logger.info("Starting to display images")
        while RUNNING:
            folder_id = db.available_folder
            if folder_id:
                images = db.get_n_images_from_folder(5, folder_id)
                for image in images:
                    if os.path.exists(image.path):
                        _logger.debug("Displaying '{}'".format(image.path))
                        feh.next_image(image.path)
                        time.sleep(configuration["image_time"])
                    else:
                        _logger.info("Removing '{}'".format(image.path))
                        db.remove_image(image)
                db.add_displayed_images([i.image_id for i in images])
            else:
                db.clear_displayed_images()
    except KeyboardInterrupt:
        _logger.info("Stopping gracefully")
    finally:
        _logger.debug("Stopping feh...")
        feh.stop()
        _logger.debug("Exiting!")

    RUNNING = False

    if usb_mounter_thread:
        usb_mounter_thread.join()

    return 0


if __name__ == "__main__":
    sys.exit(main())
