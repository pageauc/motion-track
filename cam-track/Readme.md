# cam-track.py  - Camera Movement Tracker Demo
#### A Raspberry Pi Camera Pan-Tilt Tracker using openCV2 & Video Stream Thread

YouTube Video Demo https://youtu.be/yjA3UtwbD80   
YouTube Video Code Walkthrough https://youtu.be/lkh3YbbNdYg   
RPI Forum Post https://www.raspberrypi.org/forums/viewtopic.php?p=1027463#p1027463  
Github Repo https://github.com/pageauc/motion-track/tree/master/cam-track   

###Release History
* ver 0.6 15-Aug-2016 - Initial Release
* ver 0.7 16-Aug-2016 - Added extra comments and move np import

### Program Description
This is a raspberry pi computer openCV2 program that tracks camera (pan/tilt)
 movements. It requires a RPI camera module installed and working. The program is 
written in python2 and uses openCV2.  

It captures a search rectangle from the center of a video stream tread image. 
It then locates the rectangle in subsequent images based on a score value and
returns the x y location in the image based on a threshold accuracy.  
If movement gets too close to the sides of the image or
a suitable image search match cannot be found, then another search rectangle
is selected. This data is processed to track a cumulative pixel location based on
an initial camera image center value of 0,0.    
This code could be used for a simple robotics application, movement stabilization, 
searching for an object image in the video stream rather than taking a search
rectangle from the stream itself.  Eg look for a dog.
where the camera is mounted on a moving platform or object, Etc.  

Note: This application is a demo and is currently still in development, but I 
thought it could still be useful, since I was not able to find a similar
RPI application that does this.  Will try to implement an object searcher based
on this demo.

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
    mkdir ~/cam-track
    cd ~/cam-track
    wget https://raw.github.com/pageauc/motion-track/master/cam-track/cam-track.py
    chmod +x cam-track.py  
    ./cam-track.py       # defaults to run from RPI desktop terminal session
                         # Set window_on=False if running in SSH session
                         
### Tuning
You may have to experiment with some settings to optimize performance.
If there are plain backgrounds or random motions in camera view then the
tracking values may get out of sync.

The two main variables are

#### MAX_SEARCH_THRESHOLD  default is .97
This variable sets the value for the highest accuracy for maintaining a 
lock on the search rectangle found in the stream images.  Otherwise another similar block will be returned.  
Setting this higher will force a closer match to the original search rectangle. 
If you have a unique background features then set this higher eg .98, .99 
or for a background with fewer unique features set it lower since the match criteria
will not be able to be met.  Review debug data for your environment.

#### MIN_SEARCH_THRESHOLD default is .45
This variable sets the threshold value for the lowest accuracy search result found.
If the value falls below this setting then it will force a reset to get a new
search rectangle.  This can happen if the original search rectangle is not visible 
due to lighting or being obscured by something in frame.  Review debug data
for your environment.

Use a text editor to review code for other variable settings.  Eg. 

    nano cam-track.py
    
nano editor is just a suggestion.  You can use whatever editor you are
comforable with

Have Fun Claude Pageau

YouTube Channel https://www.youtube.com/user/pageaucp

GitHub https://github.com/pageauc
