#!/bin/sh
# Convenient speed2 install.sh script written by Claude Pageau 1-Jul-2016
ver="1.6"
echo "      speed2 Install.sh script ver $ver"
echo "Install or Upgrade speed2 Object speed tracking"
echo "-----------------------------------------------"
echo "1 - Performing Raspbian System Update"
sudo apt-get -y update
echo "1 - Performing Raspbian System Upgrade"
sudo apt-get -y upgrade
echo "2 - Installing speed2 Dependencies"
sudo apt-get install -y python-opencv python-picamera python-imaging python-pyexiv2 libgl1-mesa-dri
sudo apt-get install -y fonts-freefont-ttf # Required for Jessie Lite Only
echo "3 - Create folder speed2"
cd ~
mkdir -p speed2
cd ~/speed2
echo "4 - Downloading github repo files"
wget -O install.sh -q --show-progress https://raw.github.com/pageauc/motion-track/master/speed-track-2/install.sh
wget -O speed2.py -q --show-progress https://raw.github.com/pageauc/motion-track/master/speed-track-2/speed2.py
wget -O speed2.sh -q --show-progress https://raw.github.com/pageauc/motion-track/master/speed-track-2/speed2.sh
wget -O Readme.md -q --show-progress https://raw.github.com/pageauc/motion-track/master/speed-track-2/Readme.md
wget -q --show-progress https://raw.github.com/pageauc/motion-track/master/speed-track-2/config.py
echo "5 - Make required Files Executable"
chmod +x speed2.py
chmod +x speed2.sh
chmod +x install.sh
echo "6 - Installation Complete"
echo "-----------------------------------------------"
echo "See Readme.md for speed2 Program Requirements, Configuration and Calibration"
echo
echo "Note: If config.py already exists then new file ends with a sequence number"
echo "You should reboot RPI if there are significant Raspbian system file updates"
echo "Check speed2 variable settings in config.py"
echo "cd ~/speed2"
echo "nano config.py"
echo "You must perform a speed2 calibration procedure per Readme.md file instructions"
echo "To start speed2 perform the following while in the speed2 folder"
echo "./speed2.py"
echo
echo "Good Luck Claude" 









