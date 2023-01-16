
import subprocess

def main():
    required_packages = ["feh"]
    print("Running apt-get to install necessary packages")
    print("Packages: {}".format(",".join(required_packages)))

    subprocess.check_call(["apt-get", "install", "--yes"] + required_packages)

    service_content = """
[Desktop Entry]
Type=Application
Name=piframe
Exec=/usr/local/bin/piframe
"""

    print("Writing autostart service file")
    os.mkdir(os.path.expanduser("~/.config/"))
    os.mkdir(os.path.expanduser("~/.config/autostart"))
    with open(os.path.expanduser("~/.config/autostart/piframe.desktop"), "w+") as service_file:
        service_file.write(service_content)

    print("Reboot now")

if __name__ == "__main__":
    main()
