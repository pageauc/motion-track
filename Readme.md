# motion-track Demo
##### Raspberry Pi - python opencv2 motion tracking using picamera module
##### written by Claude Pageau
code available at https://github.com/pageauc/motion-track

Here is my YouTube video showing the demo code running on a Raspberry Pi B2
http://youtu.be/09JS7twPBsQ
RPI forum post here 
https://www.raspberrypi.org/forums/viewtopic.php?p=790082#p790082

#### Speed Track - Object speed camera based on motion tracking
See https://github.com/pageauc/motion-track/blob/master/speed-track/speed_track.md
for my new speed track - an object speed tracking program demo using similar
opencv code as motion-track.py
Speed track YouTube video here  https://youtu.be/eRi50BbJUro

#### Note this program is for demonstration purposes only

#### NEW 18-May-2016 - track2.py (multi processor motion tracking demo)
Added track2.py Demo of multi processor motion tracking.
This uses one processor for camera stream, second for opencv motion tracking and
the third for program logic.  Run track2.py in a local RPI GUI terminal window
to display the opencv image window showing motion tracking stream.  The 
motion track data will be displayed in the terminal window. I used an object
on a string to test tracking.  This is amazingly fast.
Note this needs to be run on a quad core RPI for max speed. Use htop to
monitor cpu usage. Change window_on variable to run in a console/ssh session
This code can be used as a starting point for a motion tracking project
See code comments for details and installation requirements

    # Basic installation instructions (default is GUI desktop mode)
    wget https://raw.github.com/pageauc/motion-track/master/track2.py
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y python-opencv python-picamera
    chmod +x track2.py
    ./track2.py    

#### Motion Tracking Demo (single processor version)

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
    
if you get an opengl error then see this article about installing opengl on 
a RPI P2  https://www.raspberrypi.org/blog/another-new-raspbian-release/

Otherwise install opengl support library per following command then reboot.

    sudo apt-get install libgl1-mesa-dri
    
I have set window_on = True so the opencv status windows can display camera
motion images and a circle marking x,y coordinates as well as
the threshold images.  The circle diameter can be change using CIRCLE_SIZE
variable.  
You can set window_on = False if you need to run from SSH session.  If debug
= True then status information will be displayed without a GUI desktop session.

I have added motion3-track.py for use with python3 and OpenCV3 FYI. Only
the cv2.findContour line needed to be changed due to OpenCV3 syntax difference.
Steps for installing OpenCV3 can be found here
https://www.raspberrypi.org/forums/viewtopic.php?p=792568&sid=adf009c84bee379cd08b377168535477#p792568

Good Luck  Claude ...




