#!/bin/sh
# writtem by Claude Pageau 
# Script to run speed2.py in background available here
# wget https://raw.github.com/pageauc/motion-track/master/speed-track-2/speed2.sh
# launch from command line or via entry in /etc/rc.local file
# You may have to change sleep delay if it does not run properly in rc.local
# make sure to make this script executable
# chmod +x speed2.sh
# and also
# chmod +x speed2.py
# NOTE : This script can be used as a generic launcher by changing
#        the parameters below
progpath=/home/pi/speed2
progname=speed2.py
proglog=speed2.log

if [ -z "$(ps -ef | grep $progname | grep -v grep)" ]
then
   echo "Start $progname   Waiting 10 seconds"
   # delay for boot to complete if running from /etc/rc.local
   sleep 10
   echo "Startin speed2.py in background"
   #/home/pi/speed2/speed2.py &
   # If you want to redirect output then comment out above and uncomment below
   python -u $progpath/$progname  > $progpath/$proglog &
   echo "speed2.py started per process PID below"
   ps -ef | grep $progname | grep -v grep
else
  echo "speed2.py Already Running"
  ps -ef | grep $progname | grep -v grep
  echo
  echo "To end task kill PID above eg sudo kill 1234"
fi
echo "Done"
exit
