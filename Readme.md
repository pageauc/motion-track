#Raspberry Pi Motion Tracking
### Raspberry Pi - python opencv2 motion tracking using picamera module written by Claude Pageau

### motion-track.py - Motion Track Demo - Basic concept of tracking moving objects
This Demo program detects motion in the field of view and uses opencv to calculate the 
largest contour above a minimum size and return its x,y coordinate. 
* Motion Track Demo YouTube Video http://youtu.be/09JS7twPBsQ  
* GitHub Repo https://github.com/pageauc/motion-track
* RPI forum post https://www.raspberrypi.org/forums/viewtopic.php?p=790082#p790082  

## Other Raspberry Pi Projects based on motion tracing 

#### rpi-speed-camera - Object (vehicle) speed camera based on motion tracking
Tracks vehicle speeds or other moving objects in real time and records image 
and logs data. Now improved using threading for video stream and clipping of 
area of interest for greater performance.  
* Speed Camera YouTube Video https://youtu.be/eRi50BbJUro  
* GitHub Repo https://github.com/pageauc/rpi-speed-camera
* RPI forum post https://www.raspberrypi.org/forums/viewtopic.php?p=1004150#p1004150  

#### cam-track.py - Tracks camera x y movements
Uses a clipped search image rectangle to search subsequent video stream images and returns
the location. Can be used for tracking camera x y movements for stabilization,
robotics, Etc.   
* cam-track YouTube Video https://www.youtube.com/edit?video_id=yjA3UtwbD80   
* Code Walkthrough YouTube Video https://youtu.be/lkh3YbbNdYg     
* GitHub Repo https://github.com/pageauc/motion-track/tree/master/cam-track     
* RPI Forum Post https://www.raspberrypi.org/forums/viewtopic.php?p=1027463#p1027463   

#### hotspot-game.py - A simple motion tracking game
The game play involves using streaming video of body motion to get as many hits 
as possible inside shrinking boxes that randomly move around the screen. 
Position the camera so you can see body motions either close or standing. 
Pretty simple but I think kids would have fun with it and they just might 
take a look at the code to see how it works, change variables or game logic.      
* hotspot YouTube Video https://youtu.be/xFl3lmbEO9Y   
* GitHub hotspot-game Repo https://github.com/pageauc/hotspot-game      
* RPI Forum Post https://www.raspberrypi.org/forums/viewtopic.php?p=1026124#p1026124   

### Introduction
I did quite a bit of searching on the internet, github, etc, but could not
at the time find a similar python picamera implementation that returns x,y coordinates of
the most dominate moving object in the frame although some came close.  

###Prerequisites
Requires a Raspberry Pi computer running with an up-to-date raspbian distro and a
RPI camera module installed and configured. The dependencies below may be 
required depending on your previous installs.

    cd ~
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install python-opencv python-picamera
    mkdir -p motion-track
    cd motion-track    
    wget https://raw.github.com/pageauc/motion-track/master/motion-track.py
    chmod +x motion-track.py
    ./motion_track.py

From GUI desktop Terminal session Use nano to edit motion_track.py and change variable window_on=True ctrl-x y to save.
Start up a desktop GUI session and run the code from IDLE or open a terminal console and run 

    python ./motion-track.py
    
if you get an opengl error then see this article about installing opengl on 
a RPI P2  https://www.raspberrypi.org/blog/another-new-raspbian-release/

Otherwise install opengl support library per following command then reboot.

    sudo apt-get install libgl1-mesa-dri
    
Set variable window_on = True so the opencv status windows can display camera
motion images and a circle marking x,y coordinates as well as
the threshold images.  The circle diameter can be change using CIRCLE_SIZE
variable.  
You can set window_on = False if you need to run from SSH session.  If debug
= True then status information will be displayed without a GUI desktop session.

I have added motion3-track.py for use with python3 and OpenCV3 FYI. Only
the cv2.findContour line needed to be changed due to OpenCV3 syntax difference.
Steps for installing OpenCV3 can be found here
https://www.raspberrypi.org/forums/viewtopic.php?p=792568&sid=adf009c84bee379cd08b377168535477#p792568

## New track2.py 
#### 18-May-2016 - track2.py (multi processor motion tracking demo)

Added track2.py Demo of multi processor motion tracking.
This uses one processor thread for camera stream, second for opencv motion tracking and
the third for program logic.  Run track2.py in a local RPI GUI terminal window
to display the opencv image window showing motion tracking stream.  The 
motion track data will be displayed in the terminal window. I used an object
on a string to test tracking.  This is amazingly fast.
Note This will run fast on a single core RPI but best speed run on a quad core with no gui. Use htop to monitor cpu usage. Change window_on variable to run in a console/ssh session
This code can be used as a starting point for a motion tracking project
See code comments for details and installation requirements

    # Basic installation instructions (default is GUI desktop mode)
    wget https://raw.github.com/pageauc/motion-track/master/track2.py
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y python-opencv python-picamera
    chmod +x track2.py
    ./track2.py
    
Note currently this code will fail after a while when in gui mode due to I believe is a Raspbian library memory issue 
terminal only mode should be OK.

### Credits
Some of this code is based on a YouTube tutorial by
Kyle Hounslow using C here - https://www.youtube.com/watch?v=X6rPdRZzgjg

Good Luck  Claude ...




