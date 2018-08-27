
import logging
import os
import sys
import threading
import time

import psutil
import yaml

from . import db_wrapper
from . import feh_runner
from . import x_wrapper

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)
RUNNING=True


def image_finder(db_filename, configuration):
    global RUNNING

    db = db_wrapper.DbWrapper(db_filename)
    while RUNNING:
        images = []
        for mountpoint in configuration["mountpoints"]:
            if os.path.exists(mountpoint):
                _logger.debug(f"Scanning {mountpoint}")
                for root, dirs, files in os.walk(mountpoint):
                    for filename in (os.path.join(root, f) for f in files):
                        _, ext = os.path.splitext(filename)
                        if ext.lower()[1:] in configuration["extensions"]:
                            _logger.debug(f"Adding image {filename}")
                            images.append(filename)
        try:
            db.add_images(*tuple(images))
        except:
            RUNNING = False
        time.sleep(5)


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

    db = db_wrapper.DbWrapper(db_filename, init_script_filename)
    try:
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
    finally:
        _logger.debug("Stopping feh...")
        feh.stop()
        _logger.debug("Exiting!")

    RUNNING = False

    return 0


if __name__ == "__main__":
    sys.exit(main())
