#!/usr/bin/env python

progName = "track2.py version 1.5"

"""
track2 written by Claude Pageau pageauc@gmail.com
Raspberry (Pi) - python opencv2 Speed tracking using picamera module

This is a raspberry pi python opencv2 motion tracking demonstration program.
It will detect motion in the picamera field of view and use opencv to calculate the
largest contour and return its x,y coordinate.  

This uses multi threading to split the work up and speed up motion tracking.
  
Some of this code is based on a YouTube tutorial by
Kyle Hounslow using C here https://www.youtube.com/watch?v=X6rPdRZzgjg

Thanks to Adrian Rosebrock jrosebr1 at http://www.pyimagesearch.com 
for the PiVideoStream Class code available on github at
https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py

Here is a my YouTube video demonstrating a previous speed tracking demo
program using a Raspberry Pi B2 https://youtu.be/09JS7twPBsQ

Requires a Raspberry Pi with a RPI camera module installed and configured

Install Dependencies from a logged in SSH session per commands below

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python-opencv python-picamera

to monitor detailed RPI cpu and memory usage install htop per

sudo apt-get install htop -y

Run htop in a second ssh terminal session to monitor usage statistics

Note - This is demonstration code that can be used in another project

Regards Claude ..

"""

CAMERA_VFLIP=True
CAMERA_HFLIP=False

gui_window_on=True

# import required packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import time

#----------------------------------------------------------------------------------------------------------------
class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=100, rotation=0, hflip=False, vflip=False):
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
        
#----------------------------------------------------------------------------------------------------------------
class PiVideoTrack:
    def __init__(self, min_area=5, blur_size=10, threshold_sensitivity=25, resolution=(320, 240), framerate=32, rotation=0, hflip=False, vflip=False):
        # initialize the camera and stream
        self.min_area = min_area
        self.first_image = True
        self.track = None
        self.blur_size = blur_size
        self.threshold_sensitivity=threshold_sensitivity
        self.image = None
        self.stopped = False
        
        self.mt_xy = []
        self.vs = PiVideoStream().start()
 #      self.vs.camera.framerate = framerate  Note this does not work since video already running
        self.vs.camera.rotation = rotation
        self.vs.camera.hflip = hflip
        self.vs.camera.vflip = vflip       
        time.sleep(2.0)         # allow the camera to warmup
        
    def start(self):
        # start the thread to read frames from the video stream
        self.tm = Thread(target=self.update, args=())
        # self.tm.daemon = True
        self.tm.start()
        return self

    def update(self):
        while True:                  
            # initialize variables          
            self.motion_found = False
            self.biggest_area = self.min_area
            # grap stream image
            self.image = self.vs.read()
            if self.first_image:
                # initialize grayimage1. Only needs to be done once                    
                self.grayimage1 = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                self.first_image = False 
            else:
                # cv2.imwrite("second.jpg",self.image) 
                # Convert to gray scale, which is easier
                self.grayimage2 = cv2.cvtColor( self.image, cv2.COLOR_BGR2GRAY )
                # Get differences between the two greyed images
                self.differenceimage = cv2.absdiff( self.grayimage1, self.grayimage2 )
                # Blur difference image to enhance motion vectors
                self.differenceimage = cv2.blur( self.differenceimage,(self.blur_size,self.blur_size ))
                # Get threshold of blurred difference image based on THRESHOLD_SENSITIVITY variable
                retval, self.thresholdimage = cv2.threshold( self.differenceimage,self.threshold_sensitivity,255,cv2.THRESH_BINARY )
                # Get all the contours found in the threshold image
                self.contours, hierarchy = cv2.findContours( self.thresholdimage,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )
                # Update grayimage1 to grayimage2 ready for next image2
                self.grayimage1 = self.grayimage2  # get ready for next loop update
                self.motion_found = False
                self.biggest_area = self.min_area       
                # find contour with biggest area
                for c in self.contours:             
                    # get area of next contour
                    self.found_area = cv2.contourArea(c)
                    if self.found_area > self.biggest_area:
                        self.motion_found = True
                        self.biggest_area = self.found_area
                        ( x, y, w, h ) = cv2.boundingRect(c)
                 
                if self.motion_found:                  
                    self.mt_xy = [ int(x), int(y), int(h), int(w) ]
                    self.cur_image = self.image
                else:
                    self.mt_xy = []
                           
                # if the thread indicator variable is set, stop the thread
                # and resource camera resources
                if self.stopped:
                    self.vs.stop()
                    return
                    
    def read(self):
        # return current motion position data
        return self.mt_xy
        
    def getimage(self):    
        # return current motion image
        return self.image

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True   

#-----------------------------------------------------------------------------------------------    
if __name__ == '__main__':
    try:
        # Note - This script will track position of the largest moving object in the frame
        # and return the x, y, h, w data that can be used as input for further logic

        window_on = gui_window_on     # display opencv window on local GUI desktop
        size_circle = 8
        size_line = 1       
        
        # setup fps speed variables
        fps_counter = 0
        fps_start = time.time()
        fps = 0   
        
        print ("\033c")    # Clear Screen
        print("\033[4;1H%s - written by Claude Pageau ..." % progName)
        mt = PiVideoTrack().start()     # initialize instance of motion tracking
        mt.vs.camera.hflip = CAMERA_HFLIP       # Flip camera image horizontally if required
        mt.vs.camera.vflip = CAMERA_VFLIP       # Flip camera image vertically if required
        mt.min_area = 100               # Set minimum area sq-px of object to be tracked
        print("\033[5;1HStart Scanning for Motion ...")
        print("\033[6;1H         [ x, y, h, w ]")
        while True:
            # Calculate fps
            if fps_counter > 100:
                 fps = int( fps_counter / (( time.time() - fps_start)))
                 fps_start = time.time()
                 fps_counter = 0
            else:
                fps_counter +=1
                
            mo_xy = mt.read()   # This data can be used for further processing logic
            mo_image = mt.getimage()  # Get frame from motion track thread
            print("\033[7;1HMotion @ "+ str(mo_xy)+ "                   ")
            if len(mo_xy)>0:
                cx = int( mo_xy[0] + mo_xy[2] / 2 )
                cy = int( mo_xy[1] + mo_xy[3] / 2 )
                print("\033[8;1HCenter @ "+ str( cx )+", "+ str( cy ) + "                   ") 
                if window_on:
                    # Put circle at center of biggest contour
                    cv2.circle(mo_image,( cx, cy ),size_circle,(0,255,0), size_line)        
            else:
                print("\33[8;1HCenter @                           ") 
                print("\33[9;1HSpeed  @ %i fps                 " % ( fps ))
            
            if window_on:                
                cv2.imshow('Press q in window to Quit', mo_image)    
                # Close Window if q pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

    finally: 
        mt.stop()
        print("")
        print("+++++++++++++++++++++++++++++++++++")
        print("%s - Exiting Program" % progName)
        print("+++++++++++++++++++++++++++++++++++")
        print("")                           
                            


