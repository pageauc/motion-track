# hotspot-game.py - HOTSPOT MOTION TRACKING GAME
#### A Raspberry Pi Camera Motion Tracking Game using Threaded Video Stream, OpenCV2 and Python2

### Program Description
This is a raspberry pi computer openCV2 motion tracking game.
It is written in python and uses openCV2 to detect and track motion.
The game is written in python and uses a Raspberry Pi camera in video
streaming mode.  Motion is tracked and activates menu's and game play.
Can be played by one or two players and high score is saved.  

The game play involves using body motion to get as many hits as possible
inside shrinking boxes that randomly move around the screen.  Pretty simple
but I think kids would have fun with it and just might take a look at the 
code to see how it works, change variables or game logic.

You will need the raspberry pi computer connected to a monitor or HD Television
via HDMI cable. The program is run from the RPI GUI desktop in an opencv window.
The window can be resize using the WINDOW_BIGGER resize multiplier variable.
Use nano to edit if desired.
 
* hotspot-game YouTube video here https://youtu.be/xFl3lmbEO9Y
* github repo here https://github.com/pageauc/motion-track/tree/master/hotspot-game
* motion-track YouTube video here using RPI B2 https://youtu.be/09JS7twPBsQ

#### Credits
Some of this code is based on a YouTube tutorial by
Kyle Hounslow using C here https://www.youtube.com/watch?v=X6rPdRZzgjg

Thanks to Adrian Rosebrock jrosebr1 at http://www.pyimagesearch.com 
for the PiVideoStream Class code available on github at
https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py

### Quick Setup
Install dependencies and program per the following
login via SSH or use a desktop terminal session and perform the following

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y python-opencv python-picamera
    sudo apt-get install -y fonts-freefont-ttf # Required for Jessie Lite Only
    cd ~
    mkdir hotspot-game
    cd ~/hotspot-game
    wget https://raw.github.com/pageauc/motion-track/master/hotspot-game/hotspot-game.py
    chmod +x hotspot-game.py
    python ./hotspot-game.py

    
### Settings

Variable values are stored in the hotspot-game.py file. Use the nano editor to
modify these settings per the comments.  Most settings should be OK and should
not need to be changed. Others may need to be fine tuned. The openCV settings most
likely won't need to be changed unless you are familiar with them.

Have Fun

Claude Pageau

YouTube Channel https://www.youtube.com/user/pageaucp  
GitHub https://github.com/pageauc
