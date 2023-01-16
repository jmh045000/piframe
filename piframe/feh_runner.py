
import logging
import os
import subprocess
import time

_logger = logging.getLogger("feh_wrapper")

class FehRunner(object):
    blackhole = open("/dev/null", "w")

    def __init__(self, feh_options):
        self.last_proc = None
        self.proc = None
        self.command_base = ["feh"] + feh_options
        self.command_env = {k: os.environ[k] for k in os.environ}
        self.command_env["HOME"] = os.path.expanduser("~")
        self.command_env["DISPLAY"] = ":0"

    @property
    def running(self):
        return self.proc is not None and self.proc.poll() is None

    def next_image(self, image_path):
        if self.last_proc:
            self.last_proc.kill()
        if self.running:
            self.last_proc = self.proc
        self.proc = subprocess.Popen(
            self.command_base + [image_path],
            env=self.command_env,
            #stdout=subprocess.PIPE,
            #stderr=subprocess.PIPE,
        )
        if self.proc.poll() is not None:
            stdout, stderr = self.proc.communicate()
            _logger.error("feh exited unexpectedly.  rc={}, stdout='{}', stderr='{}'".format(self.proc.returncode, stdout, stderr))

    def stop(self):
        if self.running:
            if self.last_proc:
                self.last_proc.kill()
            self.proc.kill()
