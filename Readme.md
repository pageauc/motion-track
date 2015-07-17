# motion-track Demo
##### Raspberry Pi - python opencv2 motion tracking using picamera module
##### written by Claude Pageau
code available at https://github.com/pageauc/motion-track

Here is my YouTube video showing the demo code running on a Raspberry Pi B2
http://youtu.be/09JS7twPBsQ
#### Note this program is for demonstration purposes only

motion-track.py is a raspberry pi python opencv2 (computer vision) 
motion tracking demonstration program.

It will detect motion in the field of view and use opencv2 to compare
images and calculate a threshold image and related contours. It will
determine the largest contour and return it's x,y coordinates.
I will implement similar code in a RPI robotics project, but thought the code
would be useful for other users as a starting point or as part of an 
existing project.

I did quite a bit of searching on the internet, github, etc, but could not
find a similar python picamera implementation that returns x,y coordinates of
the most dominate moving object in the frame although some came close.  

Some of this code is based on a YouTube tutorial by
Kyle Hounslow using C here - https://www.youtube.com/watch?v=X6rPdRZzgjg

####Prerequisites
Requires a Raspberry Pi computer running an up-to-date raspbian distro and a
RPI camera module installed and configured. The dependencies below may be 
required depending on your previous installs.

    cd ~
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install python-opencv python-picamera
    mkdir motion-track
    cd motion-track    
    wget https://raw.github.com/pageauc/motion-track/master/motion-track.py
    
start up a desktop GUI session and run the code from IDLE or open a 
terminal console and run 

    python ./motion-track.py
    
I have set debug=True so the opencv status windows will display camera
motion images and a circle marking x,y coordinates as well as
the threshold images

Good Luck  Claude ...




