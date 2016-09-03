#!/usr/bin/env python

progname = "cam-track-multi.py"
ver = "version 0.9"

"""
Multi Threaded version of cam-track.py
cam-track written by Claude Pageau pageauc@gmail.com
Raspberry (Pi) - python opencv2 camera pan/tilt tracking using picamera module

This is a raspberry pi python opencv2 camera tracking demonstration program.
It takes a sample search rectangle from center of video stream image
and tracks its position based on a percent accuracy at maxLoc.
As the camera pans and tilts.  The cumulative position is displayed.

I will work on converting position based on 360 degree camera movement.
This is still very much a work in progress but I thought it would be
useful for others who might want a simple way to track camera movement.
Note the program can get confused by plain surroundings or some
other movements in the frame although this can be tuned out somewhat
using cam_move_x and cam_move_y global variables

This runs under python2 and openCV2 

installation
-------------
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python-opencv python-picamera
mkdir ~/cam-track
cd ~/cam-track
wget https://raw.github.com/pageauc/motion-track/master/cam-track/cam-track.py
chmod +x cam-track.py  
./cam-track.py       # defaults to run from RPI desktop terminal session

Good Luck  Claude ...

"""
print("%s %s using python2 and OpenCV2" % (progname, ver))
print("Camera movement (pan/tilt) Tracker using openCV2 image searching")
print("Loading Please Wait ....")

# import the necessary packages
import time
import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from operator import itemgetter
import numpy as np

#-----------------------------------------------------------------------------------------------  
# Global Variable Settings
debug = False       # Set to False for no data display
window_on = False  # Set to True displays opencv windows (GUI desktop reqd)
fps_on = False     # Display fps (not implemented)

# Sets the maximum x y pixels that are allowed to reduce effect of objects moving in frame
cam_move_x = 12    # Max number of x pixels in one move
cam_move_y = 8    # Max number of y pixels in one move 

# OpenCV Settings
show_search_box = True   # show outline of current search box on main window
show_search_rect = False # show rectangle search_rect_1 window
show_circle = True      # show a circle otherwise show bounding rectangle on window
CIRCLE_SIZE = 3         # diameter of circle to show motion location in window
WINDOW_BIGGER = 2.0     # increase the display window size
MAX_SEARCH_THRESHOLD = .96  # default=.97 Accuracy for best search result of search_rect in stream images
LINE_THICKNESS = 1      # thickness of bounding line in pixels
CV_FONT_SIZE = .25      # size of font on opencv window default .5

# Line Colours
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)

# Camera Settings
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CAMERA_HFLIP = False
CAMERA_VFLIP = True
CAMERA_ROTATION=0
CAMERA_FRAMERATE = 35  # framerate of video stream.  Can be 100+ with new R2 RPI camera module
FRAME_COUNTER = 1000   # used by fps

#-----------------------------------------------------------------------------------------------  
# Create a Video Stream Tread
class PiVideoStream:
    def __init__(self, resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=CAMERA_FRAMERATE, rotation=0, hflip=False, vflip=False):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.rotation = rotation
        self.camera.framerate = framerate
        self.camera.hflip = hflip
        self.camera.vflip = vflip
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

class PiCamTrack:
    def __init__(self, resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=CAMERA_FRAMERATE, rotation=0, hflip=False, vflip=False):

        # Process steam images to find camera movement 
        # using an extracted search rectangle in the middle of one frame
        # and find location in subsequent images.  Grap a new search rect
        # as needed based on nearness to edge of image or percent probability
        # of image search result Etc.

        if WINDOW_BIGGER > 1:  # Note setting a bigger window will slow the FPS
            self.big_w = int(CAMERA_WIDTH * WINDOW_BIGGER)
            self.big_h = int(CAMERA_HEIGHT * WINDOW_BIGGER) 
        
        # initialize the search window (rect) variables 
        self.image_cx = int(CAMERA_WIDTH/2)   # x center of image
        self.image_cy = int(CAMERA_HEIGHT/2)  # y center of image       
        self.sw_w = int(CAMERA_WIDTH/4)    # search window width
        self.sw_h = int(CAMERA_HEIGHT/4)   # search window height
        self.sw_buf_x = int(self.sw_w/4)        # buffer to left/right of image
        self.sw_buf_y = int(self.sw_h/4)        # buffer to top/bot of image
        self.sw_x = (self.image_cx - self.sw_w/2)       # top x corner of search rect
        self.sw_y = (self.image_cy - self.sw_h/2)       # top y corner of search rect
        self.sw_maxVal = MAX_SEARCH_THRESHOLD  # Threshold Accuracy of search in image
       
        # Grab a Video Steam image and initialize search rectangle
        self.cam_cx1 = self.image_cx    # Set Cam x center start position
        self.cam_cy1 = self.image_cy    # Set Cam y center start position
        self.cam_pos_x = 0   # initialize cam horizontal movement tracker
        self.cam_pos_y = 0   # initialize cam vertical movement tracker
        self.search_reset = False  # Reset search window
        self.stopped = False 
        global cam_position
        cam_position = (0,0)    # Position of Camera
        self.image1 = None
        
    def start(self):
        ct = Thread(target=self.update, args=())
        ct.daemon = True
        ct.start()
        return self  
         
    def update(self):
        global cam_position
        # Setup Video Stream Thread
        vs = PiVideoStream().start()        
        vs.camera.rotation = CAMERA_ROTATION
        vs.camera.hflip = CAMERA_HFLIP
        vs.camera.vflip = CAMERA_VFLIP
        time.sleep(2.0)    # Let camera warm up          
        self.image1 = vs.read()   # initialize first image
        self.search_rect = (self.image1[self.sw_y:self.sw_y + self.sw_h, 
                                        self.sw_x:self.sw_x + self.sw_w])  # Initialize centre search rectangle                               
        keep_processing = True        
        while keep_processing:
            self.image1 = vs.read()  # capture a new image1 from video stream thread
            # Look for search_rect in this image and return result
            self.result = cv2.matchTemplate( self.image1, self.search_rect, cv2.TM_CCORR_NORMED)
            # Process result to return probabilities and Location of best and worst image match
            self.minVal, self.maxVal, self.minLoc, self.maxLoc = cv2.minMaxLoc(self.result)  # find search rect match in new image
            # Get the center of the best matching result of search
            self.cam_cx2, self.cam_cy2 = get_center( self.maxLoc[0], self.maxLoc[1], self.sw_w, self.sw_h ) 

            # Update cumulative camera tracking data and check max_move
            if self.cam_cx2 <> self.cam_cx1:
                if abs(self.cam_cx2 - self.cam_cx1) > cam_move_x:
                    self.search_reset = True  
                    if debug:
                        print("    cam_move_x=%i Exceeded %i" 
                                 % (abs(self.cam_cx2 - self.cam_cx1), cam_move_x))                        
                else:                
                    self.cam_pos_x = self.cam_pos_x + (self.cam_cx1 - self.cam_cx2)
                    self.cam_cx1 = self.cam_cx2
                
            if self.cam_cy2 <> self.cam_cy1:
                if abs(self.cam_cy2 - self.cam_cy1) > cam_move_y:
                    self.search_reset = True            
                    if debug:
                        print("    cam_move_y=%i Exceeded %i" 
                                 % (abs(self.cam_cy2 - self.cam_cy1), cam_move_y))            
                else:                
                    self.cam_pos_y = self.cam_pos_y + (self.cam_cy1 - self.cam_cy2)
                    self.cam_cy1 = self.cam_cy2
                
            # Check if search rect is well inside image1
            # and maxVal and minVal are above threshold
            if ( self.maxLoc[0] < self.sw_buf_x 
              or self.maxLoc[0] > CAMERA_WIDTH - (self.sw_buf_x + self.sw_w)
              or self.maxLoc[1] < self.sw_buf_y 
              or self.maxLoc[1] > CAMERA_HEIGHT -(self.sw_buf_y + self.sw_h)
              or self.maxVal < self.sw_maxVal):
                self.search_reset = True

            if self.search_reset:            
                if debug:
                    print("    Reset search_rect cur_cx=%i cam_pos_x=%i cur_cy=%i cam_pos_y=%i" 
                                               % (self.cam_cx2, self.cam_cy2, self.cam_pos_x, self.cam_pos_y))        
                self.search_rect = (self.image1[self.sw_y:self.sw_y + self.sw_h, 
                                                self.sw_x:self.sw_x + self.sw_w])              
                self.cam_cx1 = self.image_cx
                self.cam_cy1 = self.image_cy    
                self.cam_cx2 = self.cam_cx1         
                self.cam_cy2 = self.cam_cy1
                self.search_reset = False               

            cam_position = (self.cam_pos_x, self.cam_pos_y)
            
            if self.stopped:
                self.vs.stop()
                keep_processing = False
                return
                
            if debug: 
                print("CamPos (%i, %i) cam_pos_x, cam_pos_y" % ( self.cam_pos_x, self.cam_pos_y, ))
                print(" maxLoc   maxVal   minLoc   minVal")
                print self.maxLoc, "{0:0.4f}".format(self.maxVal) ,  self.minLoc ,"{0:0.4f}".format(self.minVal)   
         
    def read(self):
        return cam_position

    def stop(self):
        self.stopped = True    
      
#-----------------------------------------------------------------------------------------------     
def get_center(x,y,w,h):
    return int(x+w/2), int(y+h/2)    
             
#-----------------------------------------------------------------------------------------------    
if __name__ == '__main__':
    try:
        ct = PiCamTrack().start()
        while True:           
            cam_pos = ct.read()
            print("Cam Pos (%i, %i)" %( cam_pos[0], cam_pos[1]))          

    finally:
        print("")
        print("+++++++++++++++++++++++++++++++++++")
        print("%s %s - Exiting" % (progname, ver))
        print("+++++++++++++++++++++++++++++++++++")
        print("")                                



