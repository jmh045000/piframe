
import subprocess

def main():
    required_packages = ["xorg", "feh", "pmount"]
    print("Running apt-get to install necessary packages")
    print("Packages: {}".format(",".join(required_packages)))

    subprocess.check_call(["apt-get", "install", "--yes"] + required_packages)

    service_content = """
[Unit]
Description=Pi Photo Frame
Documentation=http://github.com/jmh045000/piframe

[Service]
ExecStart=/usr/local/bin/piframe
Restart=on-failure

[Install]
WantedBy=multi-user.target"""

    print("Writing systemd service file")
    with open("/etc/systemd/system/piframe.service", "w+") as service_file:
        service_file.write(service_content)

    print("Enabling systemd service")
    subprocess.check_call(["systemctl", "daemon-reload"])
    subprocess.check_call(["systemctl", "enable", "piframe"])

if __name__ == "__main__":
    main()
