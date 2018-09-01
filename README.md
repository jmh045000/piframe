# piframe
A photo frame application for the raspberry pi

# first time setup

Run the following commands to get it up and running after installing raspbian stretch

```
sudo apt-get install python3 python3-pip
sudo python3 -m pip install git+https://github.com/jmh045000/piframe.git
sudo piframe-firstrun
```

Then reboot the raspberry and insert USB sticks with photos

# algorithm

1. Scan `/dev` for any files matching `/dev/sd[a-z]\d+` and `pmount` them in background
2. Scan all of `/media` and `/mnt` for images with extentions matching configuration
3. Start X server in background
4. Find a folder with undisplayed images, and display 5 images from that folder.
5. Repeat 4 until out of images.  Once out, clear all memory of displayed images and restart 4
