# cam-track.py
####  A Raspberry Pi opencv2 camera movement tracking using Video Streaming and Threading

###Release History
* ver 0.6 15-Aug-2016 - Initial Release

### Program Description
This is a raspberry pi computer openCV2 camera pan/tilt) movements. It requires
a RPI camera module installed and working. The program is 
written in python2 and uses openCV2.  It capture a search rectangle
from the center of the video stream. It then locates the rectangle in the
subsequent images based on a score value and returns the x y location on
the image.  If movement gets too close to the sides of the image or
a suitable image search match cannot be found, then another search rectangle
is selected. This is processed to track a cumulative pixel location base on
center of the camera image with an initial location of 0,0.    
This could be used for a simple robotics application or where the camera is 
mounted on a moving platform.  

This application is a demo and is currently still in development but I 
thought it could still be useful since I was not able to find a similar
RPI application that does this.

Thanks to Adrian Rosebrock jrosebr1 at http://www.pyimagesearch.com 
for the PiVideoStream Class code available on github at
https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py

### Setup
Requires a Raspberry Pi computer with a RPI camera module installed, configured
and tested to verify it is working. I used a RPI model B2 but a B+ , 3 or 
earlier will work OK. A quad core processor will greatly improve performance
due to threading

From logged in RPI SSH session or console terminal perform the following.  

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y python-opencv python-picamera
    sudo apt-get install -y fonts-freefont-ttf # Required for Jessie Lite Only
    mkdir ~/cam-track
    cd ~/cam-track
    wget https://raw.github.com/pageauc/motion-track/master/cam-track/cam-track.py
    chmod +x cam-track.py  
    ./cam-track.py       # defaults to run from RPI desktop terminal session
  
#### Tuning
You may have to experiment with some settings to optimize performance.
If there are plain backgrounds or random motions in camera view then the
tracking values may get out of sync.

The two main variables are

sw_maxLoc  -  default is .95 This sets the value for the highest accuracy for
the search rectangle found in the stream images.

sw_minVal  -  default is .45  This sets the
Have Fun

See program variables for other settings

Claude Pageau

YouTube Channel https://www.youtube.com/user/pageaucp

GitHub https://github.com/pageauc
