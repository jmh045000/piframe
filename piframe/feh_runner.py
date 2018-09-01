
import os
import subprocess
import time


class FehRunner(object):
    blackhole = open("/dev/null", "w")

    def __init__(self, feh_options):
        self.last_proc = None
        self.proc = None
        self.command_base = ["feh"] + feh_options
        self.command_env = {
            "XAUTHORITY": os.path.expanduser("~/.XAuthority"),
            "DISPLAY": ":0.0",
            "HOME": os.path.expanduser("~"),
        }

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
            stdout=self.blackhole,
            stderr=self.blackhole,
        )

    def stop(self):
        if self.running:
            if self.last_proc:
                self.last_proc.kill()
            self.proc.kill()
