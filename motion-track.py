#!/usr/bin/env python
progname = "motion_track.py"
ver = "version 1.00"

"""
motion-track ver 1.00 written by Claude Pageau pageauc@gmail.com
Raspberry (Pi) - python opencv2 motion tracking using picamera module

This is a raspberry pi python opencv2 motion tracking demonstration program.
It will detect motion in the field of view and use opencv to calculate the
largest contour and return its x,y coordinate.  I will be using this for
a simple RPI robotics project, but thought the code would be useful for
other users as a starting point for a project.  I did quite a bit of
searching on the internet, github, etc but could not find a similar
implementation that returns x,y coordinates of the most dominate moving
object in the frame.  Some of this code is base on a YouTube tutorial by
Kyle Hounslow using C here https://www.youtube.com/watch?v=X6rPdRZzgjg

Here is a my YouTube video demonstrating this demo program using a
Raspberry Pi B2 https://youtu.be/09JS7twPBsQ

Requires a Raspberry Pi with a RPI camera module installed and configured
dependencies. Cut and paste command below into a terminal sesssion to
download and install motion_track demo.  Program will be installed to
~/motion-track-demo folder

curl -L https://raw.github.com/pageauc/motion-track/master/motion-track-install.sh | bash

To Run Demo

cd ~/motion-track-demo
./motion-track.py

"""
print("%s %s motion tracking using python2 or 3 and OpenCV" % (progname, ver))
print("Loading Please Wait ....")

import os
mypath=os.path.abspath(__file__)       # Find the full path of this python script
baseDir=mypath[0:mypath.rfind("/")+1]  # get the path location only (excluding script name)
baseFileName=mypath[mypath.rfind("/")+1:mypath.rfind(".")]
progName = os.path.basename(__file__)

# Check for variable file to import and error out if not found.
configFilePath = baseDir + "config.py"
if not os.path.exists(configFilePath):
    print("ERROR - Missing config.py file - Could not find Configuration file %s" % (configFilePath))
    import urllib2
    config_url = "https://raw.github.com/pageauc/motion-track/master/config.py"
    print("   Attempting to Download config.py file from %s" % ( config_url ))
    try:
        wgetfile = urllib2.urlopen(config_url)
    except:
        print("ERROR - Download of config.py Failed")
        print("   Try Rerunning the motion-track-install.sh Again.")
        print("   or")
        print("   Perform GitHub curl install per Readme.md")
        print("   and Try Again")
        print("Exiting %s" % ( progName ))
        quit()
    f = open('config.py','wb')
    f.write(wgetfile.read())
    f.close()

# Read Configuration variables from config.py file
from config import *

# import the necessary packages
import logging
import time
import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread

if debug:
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(funcName)-10s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

#-----------------------------------------------------------------------------------------------
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

#-----------------------------------------------------------------------------------------------
class WebcamVideoStream:
    def __init__(self, src=0, WEBCAM_WIDTH=320, WEBCAM_HEIGHT=240):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3,WEBCAM_WIDTH)
        self.stream.set(4,WEBCAM_HEIGHT)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                    return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

#-----------------------------------------------------------------------------------------------
def show_FPS(start_time,frame_count):
    if debug:
        if frame_count >= FRAME_COUNTER:
            duration = float(time.time() - start_time)
            FPS = float(frame_count / duration)
            logging.info("Processing at %.2f fps last %i frames", FPS, frame_count)
            frame_count = 0
            start_time = time.time()
        else:
            frame_count += 1
    return start_time, frame_count

#-----------------------------------------------------------------------------------------------
def track():
        
    # Save images to an in-program stream
    # Setup video stream on a processor Thread for faster speed
    if WEBCAM:   #  Start Web Cam stream (Note USB webcam must be plugged in)
        print("Initializing USB Web Camera ....")
        WEBCAMSRC=0
        vs = WebcamVideoStream().start()
        vs.src = WEBCAMSRC
        vs.WEBCAM_WIDTH = CAMERA_WIDTH
        vs.WEBCAM_HEIGHT = CAMERA_HEIGHT
    else:
        print("Initializing Pi Camera ....")    
        vs = PiVideoStream().start()
        vs.camera.rotation = CAMERA_ROTATION
        vs.camera.hflip = CAMERA_HFLIP
        vs.camera.vflip = CAMERA_VFLIP
    time.sleep(2.0)  # Allow cam to initialize

    if window_on:
        print("Press q in window Quits")
    else:
        print("Press ctrl-c to Quit")       
    
    if debug:
        logging.info("Start Motion Tracking ....")     
    else:
        print("Start Motion Tracking ....")     
        print("Note: Console Messages Supressed per debug=%s" % debug)
   
    big_w = int(CAMERA_WIDTH * WINDOW_BIGGER)
    big_h = int(CAMERA_HEIGHT * WINDOW_BIGGER)
    cx, cy, cw, ch = 0, 0, 0, 0   # initialize contour center variables
    frame_count = 0  #initialize for show_fps
    start_time = time.time() #initialize for show_fps
    image1 = vs.read()   # initialize image1 (done once)
    try:
        grayimage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    except:
        print("---------------- ERROR ------------------")
        print(" Problem with Camera.")
        print(" Maybe Due to Restarting Web Cam Too Soon After Shutdown")
        print(" Please Wait a Few Seconds and Try Again.")
        quit(1)
    still_scanning = True
    while still_scanning:
        # initialize variables
        motion_found = False
        biggest_area = MIN_AREA
        image2 = vs.read()  # initialize image2
        grayimage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        if show_fps:
            start_time, frame_count = show_FPS(start_time, frame_count)
        # Get differences between the two greyed images
        differenceimage = cv2.absdiff(grayimage1, grayimage2)
        grayimage1 = grayimage2  # save grayimage2 to grayimage1 ready for next image2
        differenceimage = cv2.blur(differenceimage,(BLUR_SIZE,BLUR_SIZE))
        # Get threshold of difference image based on THRESHOLD_SENSITIVITY variable
        retval, thresholdimage = cv2.threshold( differenceimage, THRESHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY )
        try:
            thresholdimage, contours, hierarchy = cv2.findContours( thresholdimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
        except:
            contours, hierarchy = cv2.findContours( thresholdimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

        if contours != ():
            total_contours = len(contours)  # Get total number of contours
            for c in contours:              # find contour with biggest area
                found_area = cv2.contourArea(c)  # get area of next contour
                # find the middle of largest bounding rectangle
                if found_area > biggest_area:
                    motion_found = True
                    biggest_area = found_area
                    (x, y, w, h) = cv2.boundingRect(c)
                    cx = int(x + w/2)   # put circle in middle of width
                    cy = int(y + h/6)   # put circle closer to top
                    cw, ch = w, h

            if motion_found:
                # Do Something here with motion data
                if window_on:
                    # show small circle at motion location
                    if SHOW_CIRCLE:
                        cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,255,0), LINE_THICKNESS)
                    else:
                        cv2.rectangle(image2,(cx,cy),(x+cw,y+ch),(0,255,0), LINE_THICKNESS)
                if debug:
                    logging.info("at cx,cy(%3i,%3i)  TC's=%2i  BC:%ix%i=%i SqPx" %
                                    (cx ,cy, total_contours, cw, ch, biggest_area))

        if window_on:
            if diff_window_on:
                cv2.imshow('Difference Image',differenceimage)
            if thresh_window_on:
                cv2.imshow('OpenCV Threshold', thresholdimage)
            if WINDOW_BIGGER > 1:  # Note setting a bigger window will slow the FPS
                image2 = cv2.resize( image2,( big_w, big_h ))
            cv2.imshow('Movement Status  (Press q in Window to Quit)', image2)

            # Close Window if q pressed while movement status window selected
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                vs.stop()
                print("End Motion Tracking")
                still_scanning = False

#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        track()
    finally:
        print("")
        print("+++++++++++++++++++++++++++++++++++")
        print("%s %s - Exiting" % (progname, ver))
        print("+++++++++++++++++++++++++++++++++++")
        print("")



