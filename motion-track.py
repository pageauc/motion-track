#!/usr/bin/env python
progname = "motion_track.py"
ver = "version 1.81"

"""
motion-track  written by Claude Pageau pageauc@gmail.com
Windows, Unix, Raspberry (Pi) - python opencv2 motion tracking
using web camera or raspberry pi camera module.

This is a python opencv2 motion tracking demonstration program.
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

This will run on a Windows, Unix OS using a Web Cam or a Raspberry Pi
using a Web Cam or RPI camera module installed and configured

To do a quick install On Raspbian or Debbian Copy and paste command below
into a terminal sesssion to download and install motion_track demo.
Program will be installed to ~/motion-track-demo folder

curl -L https://raw.github.com/pageauc/motion-track/master/motion-track-install.sh | bash

To Run Demo

cd ~/motion-track-demo
./motion-track.py

"""
print("Loading ....")
# import the necessary packages
import logging
import time
import cv2
from threading import Thread
import os
import subprocess
import sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(funcName)-10s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("%s %s motion tracking   written by Claude Pageau", progname, ver)

mypath=os.path.abspath(__file__)       # Find the full path of this python script
baseDir=mypath[0:mypath.rfind("/")+1]  # get the path location only (excluding script name)
baseFileName=mypath[mypath.rfind("/")+1:mypath.rfind(".")]
progName = os.path.basename(__file__)

# Check for variable file to import and error out if not found.
configFilePath = baseDir + "config.py"
if not os.path.exists(configFilePath):
    logging.error("Missing config.py File %s",configFilePath)
    import urllib2
    config_url = "https://raw.github.com/pageauc/motion-track/master/config.py"
    logging.info("Attempting to Download new config.py file")
    logging.info("from %s", config_url)
    try:
        wgetfile = urllib2.urlopen(config_url)
    except:
        logging.error("Download of config.py Failed")
        logging.error("Try Rerunning the motion-track-install.sh Again.")
        logging.error("or Perform GitHub curl install per Readme.md")
        logging.error("Exiting %s", progName)
        sys.exit(1)
    f = open('config.py','wb')
    f.write(wgetfile.read())
    f.close()

# Read Configuration variables from config.py file
from config import *

if not WEBCAM:
    # Check that pi camera module is installed and enabled
    camResult = subprocess.check_output("vcgencmd get_camera", shell=True)
    camResult = camResult.decode("utf-8")
    camResult = camResult.replace("\n", "")
    if (camResult.find("0")) >= 0:   # Was a 0 found in vcgencmd output
        logging.error("Pi Camera Module Not Found %s" % camResult)
        logging.error("if supported=0 Enable Camera using command sudo raspi-config")
        logging.error("if detected=0 Check Pi Camera Module is Installed Correctly")
        logging.error("Exiting %s Due to Error", progName)
        sys.exit(1)
    else:
        logging.info("Pi Camera Module is Enabled and Connected %s", camResult)

try:  # Bypass loading picamera library if not available eg. UNIX or WINDOWS
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    WEBCAM = True
    pass

if WEBCAM:
    imageW = WEBCAM_WIDTH
    imageH = WEBCAM_HEIGHT
else:
    imageW = CAMERA_WIDTH
    imageH = CAMERA_HEIGHT

# Color data for OpenCV lines and text
cvWhite = (255,255,255)
cvBlack = (0,0,0)
cvBlue = (255,0,0)
cvGreen = (0,255,0)
cvRed = (0,0,255)

mo_color = cvRed  # color of motion circle or rectangle

#-----------------------------------------------------------------------------------------------
def myStuff(x,y):
    # This is where You would put code for handling motion event(s)
    # Below is just some sample code to indicate area of movement
    quadrant = "Motion In "
    if y < imageH/2:
       quadrant = quadrant + "Top"
    else:
       quadrant = quadrant + "Bottom"

    if x < imageW/2:
       quadrant = quadrant + " Left"
    else:
       quadrant = quadrant + " Right"

    logging.info("%s quadrant", quadrant)

#-----------------------------------------------------------------------------------------------
class PiVideoStream:
    def __init__(self, resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=CAMERA_FRAMERATE, rotation=0, hflip=False, vflip=False):
        # initialize the camera and stream
        try:
           self.camera = PiCamera()
        except:
           logging.error("PiCamera Already in Use by Another Process")
           logging.error("Exiting %s Due to Error" % progName)
           sys.exit(1)
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
    def __init__(self, CAM_SRC=WEBCAM_SRC, CAM_WIDTH=WEBCAM_WIDTH, CAM_HEIGHT=WEBCAM_HEIGHT):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = CAM_SRC
        self.stream = cv2.VideoCapture(CAM_SRC)
        self.stream.set(3,CAM_WIDTH)
        self.stream.set(4,CAM_HEIGHT)
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
    image1 = vs.read()   # initialize image1 (done once)
    try:
        grayimage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    except:
        vs.stop()
        logging.error("Problem Connecting To Camera Stream.")
        logging.error("Restarting Camera.  One Moment Please .....")
        time.sleep(4)
        return

    if window_on:
        logging.info("Press q in window Quits")
    else:
        logging.info("Press ctrl-c to Quit")
    logging.info("Start Motion Tracking ....")

    if not debug:
        logging.info("Note: Console Messages Suppressed per debug=%s", debug)

    big_w = int(imageW * WINDOW_BIGGER)
    big_h = int(imageH * WINDOW_BIGGER)
    frame_count = 0  #initialize for show_fps
    start_time = time.time() #initialize for show_fps
    still_scanning = True
    while still_scanning:
        # initialize variables
        motion_found = False
        biggest_area = MIN_AREA
        image2 = vs.read()  # initialize image2
        if WEBCAM:
            if ( WEBCAM_HFLIP and WEBCAM_VFLIP):
                image2 = cv2.flip( image2, -1)
            elif WEBCAM_HFLIP:
                image2 = cv2.flip( image2, 1)
            elif WEBCAM_VFLIP:
                image2 = cv2.flip( image2, 0)
        grayimage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        if show_fps:
            start_time, frame_count = show_FPS(start_time, frame_count)
        # Get differences between the two greyed images
        differenceimage = cv2.absdiff(grayimage1, grayimage2)
        grayimage1 = grayimage2  # save grayimage2 to grayimage1 ready for next image2
        differenceimage = cv2.blur(differenceimage,(BLUR_SIZE,BLUR_SIZE))
        # Get threshold of difference image based on THRESHOLD_SENSITIVITY variable
        retval, thresholdimage = cv2.threshold(differenceimage, THRESHOLD_SENSITIVITY,
                                               255, cv2.THRESH_BINARY)
        try:
            thresholdimage, contours, hierarchy = cv2.findContours(thresholdimage,
                                                                   cv2.RETR_EXTERNAL,
                                                                   cv2.CHAIN_APPROX_SIMPLE)
        except:
            contours, hierarchy = cv2.findContours(thresholdimage,
                                                   cv2.RETR_EXTERNAL,
                                                   cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            total_contours = len(contours)  # Get total number of contours
            for c in contours:              # find contour with biggest area
                found_area = cv2.contourArea(c)  # get area of next contour
                # find the middle of largest bounding rectangle
                if found_area > biggest_area:
                    motion_found = True
                    biggest_area = found_area
                    (x, y, w, h) = cv2.boundingRect(c)
                    cxy = (int(x+w/2), int(y+h/2))   # center of contour
                    rxy=(x,y) # Top left corner of rectangle

            if motion_found:
                myStuff(cxy[0],cxy[1]) # Do Something here with motion data
                if window_on:
                    # show small circle at motion location
                    if SHOW_CIRCLE:
                        cv2.circle(image2, cxy, CIRCLE_SIZE, (mo_color), LINE_THICKNESS)
                    else:
                        cv2.rectangle(image2, rxy, (x+w, y+h),
                                                   (mo_color), LINE_THICKNESS)
                if debug:
                    logging.info("cxy(%3i,%3i) C:%2i WxH:%ix%i=%i SqPx",
                                 cxy[0] ,cxy[1], total_contours, w, h, biggest_area)

        if window_on:
            if diff_window_on:
                cv2.imshow('Difference Image', differenceimage)
            if thresh_window_on:
                cv2.imshow('OpenCV Threshold', thresholdimage)
            if WINDOW_BIGGER > 1:  # Note setting a bigger window will slow the FPS
                image2 = cv2.resize(image2, (big_w, big_h))
            cv2.imshow('Press q in Window Quits)', image2)

            # Close Window if q pressed while mouse over opencv gui window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                vs.stop()
                logging.info("End Motion Tracking")
                sys.exit(0)

#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    while True:
        try:
            # Save images to an in-program stream
            # Setup video stream on a processor Thread for faster speed
            if WEBCAM:   #  Start Web Cam stream (Note USB webcam must be plugged in)
                logging.info("Initializing USB Web Camera ....")
                vs = WebcamVideoStream().start()
                vs.CAM_SRC = WEBCAM_SRC
                vs.CAM_WIDTH = WEBCAM_WIDTH
                vs.CAM_HEIGHT = WEBCAM_HEIGHT
                time.sleep(4.0)  # Allow WebCam to initialize
            else:
                logging.info("Initializing Pi Camera ....")
                vs = PiVideoStream().start()
                vs.camera.rotation = CAMERA_ROTATION
                vs.camera.hflip = CAMERA_HFLIP
                vs.camera.vflip = CAMERA_VFLIP
                time.sleep(2.0)  # Allow PiCamera to initialize
            track()
        except KeyboardInterrupt:
            vs.stop()
            print("")
            logging.info("User Pressed Keyboard ctrl-c")
            logging.info("%s %s - Exiting", progname, ver)
            sys.exit(0)



