
import subprocess
import sys

def main():
    required_packages = ["xorg", "feh"]
    print("Running apt-get to install necessary packages")
    print("Packages: {}".format(",".join(required_packages)))

    rc = subprocess.call(["apt-get", "install", "--yes"] + required_packages)
    sys.exit(rc)
