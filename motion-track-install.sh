#!/bin/bash
# Convenient motion-track motion-track-install.sh script written by Claude Pageau 1-Jul-2016
ver="1.2"
APP_DIR='motion-track-demo'  # Default folder install location

cd ~
if [ -d "$APP_DIR" ] ; then
  STATUS="Upgrade"
  echo "Upgrade motion-track files"
else  
  echo "New motion-track Install"
  STATUS="New Install"
  mkdir -p $APP_DIR
  echo "$APP_DIR Folder Created"
fi 

cd $APP_DIR
INSTALL_PATH=$( pwd )   

# Remember where this script was launched from
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "------------------------------------------------"
echo "  motion-track-Install.sh script ver $ver"
echo "  $STATUS motion-track for Camera movement tracking"
echo "------------------------------------------------"
echo ""
echo "1 - Downloading GitHub Repo files to $INSTALL_PATH"
wget -O motion-track-install.sh -q --show-progress https://raw.github.com/pageauc/motion-track/master/motion-track-install.sh
if [ $? -ne 0 ] ;  then
  wget -O motion-track-install.sh https://raw.github.com/pageauc/motion-track/master/motion-track-install.sh
  wget -O motion-track.py https://raw.github.com/pageauc/motion-track/master/motion-track.py 
  wget -O config.py https://raw.github.com/pageauc/motion-track/master/config.py  
  wget -O Readme.md https://raw.github.com/pageauc/motion-track/master/Readme.md  
else
  wget -O motion-track.py -q --show-progress https://raw.github.com/pageauc/motion-track/master/motion-track.py
  wget -O config.py -q --show-progress https://raw.github.com/pageauc/motion-track/master/config.py    
  wget -O Readme.md -q --show-progress  https://raw.github.com/pageauc/motion-track/master/Readme.md  
fi
echo "Done Download"
echo "------------------------------------------------"
echo ""
echo "2 - Make required Files Executable"
chmod +x motion-track.py
chmod +x motion-track-install.sh
echo "Done Permissions"
echo "------------------------------------------------"
# check if system was updated today
NOW="$( date +%d-%m-%y )"
LAST="$( date -r /var/lib/dpkg/info +%d-%m-%y )"
if [ "$NOW" == "$LAST" ] ; then
  echo "4 Raspbian System is Up To Date"
  echo ""  
else
  echo ""
  echo "3 - Performing Raspbian System Update"
  echo "    This Will Take Some Time ...."
  echo ""
  sudo apt-get -y update
  echo "Done update"
  echo "------------------------------------------------"
  echo ""
  echo "4 - Performing Raspbian System Upgrade"
  echo "    This Will Take Some Time ...."
  echo ""
  sudo apt-get -y upgrade
  echo "Done upgrade"
fi  
echo "------------------------------------------------"
echo ""
echo "5 - Installing motion-track Dependencies"
sudo apt-get install -y python-opencv python-picamera
echo "Done Dependencies"
cd $DIR
# Check if motion-track-install.sh was launched from motion-track folder
if [ "$DIR" != "$INSTALL_PATH" ]; then
  if [ -e 'motion-track-install.sh' ]; then
    echo "$STATUS Cleanup motion-track-install.sh"
    rm motion-track-install.sh
  fi
fi
echo "-----------------------------------------------"
echo "6 - $STATUS Complete"
echo "-----------------------------------------------"
echo ""
echo "1. Reboot RPI if there are significant Raspbian system updates"
echo "2. Raspberry pi needs a monitor/TV attached to display game window"
echo "3. Run motion-track.py with the Raspbian Desktop GUI running"
echo "4. To start open file manager or a Terminal session then change to" 
echo "   motion-track folder and launch per commands below"
echo ""
echo "   cd ~/motion-track-demo"
echo "   ./motion-track.py"
echo ""
echo "-----------------------------------------------"
echo "See Readme.md for Further Details"
echo $APP_DIR "Good Luck Claude ..."
echo "Bye"
echo ""