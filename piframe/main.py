
import logging
import sys
import threading
import time

import db_wrapper
import feh_runner
import x_wrapper

logging.basicConfig(level=logging.DEBUG)

_logger = logging.getLogger(__name__)


def image_finder(db_filename, init_script_filename, stop_event):
    db = db_wrapper.DbWrapper(db_filename, init_script_filename)
    while not stop_event.is_set():
        time.sleep(1)
        # Need to actually ipmlement this


def main():

    config_directory = os.path.join(os.path.dirname(__file__), "config")

    db_filename = "/tmp/piframe.db"
    init_script_filename = os.path.join(config_directory, "piframe.sql")
    config_filename = os.path.join(config_directory, "config.yaml")

    feh = feh_runner.FehRunner()
    xserver = x_wrapper.XServer()

    xserver.start()

    stop_event = threading.Event()
    image_finder_thread = threading.Thread(
        target=image_finder, args=(db_filename, init_script_filename, stop_event)
    )
    image_finder_thread.start()

    db = db_wrapper.DbWrapper(db_filename, init_script_filename)
    try:
        while True:
            folder_id = db.available_folder
            if folder_id:
                images = db.get_n_images_from_folder(5, folder_id)
                for image in images:
                    _logger.debug('Displaying "%s"', image.path)
                    feh.next_image(image.path)
                    time.sleep(5)
                db.add_displayed_images([i.image_id for i in images])
            else:
                _logger.info("Clearing displayed images")
                db.clear_displayed_images()
    except KeyboardInterrupt:
        _logger.debug("Waiting for finder thread to exit...")
        feh.stop()
        stop_event.set()
        _logger.debug("Exiting!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
