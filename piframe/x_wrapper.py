
import os
import pwd
import subprocess
import threading


class XServer(object):
    blackhole = open("/dev/null", "w")

    def __init__(self):
        if os.geteuid() != 0:
            raise RuntimeError("Must run as root to start X")
        self.command = ["X", "-s", ":0.0", "-dpms", "-nocursor", "-quiet"]
        self.proc = None

    @property
    def running(self):
        return self.proc is not None and self.proc.poll() is None

    def start(self):
        if not self.running:
            self.proc = subprocess.Popen(
                self.command, stdout=self.blackhole, stderr=self.blackhole
            )
