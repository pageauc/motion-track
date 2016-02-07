#!/usr/bin/env python

progname = "motion_track.py"
ver = "version 0.7"

"""
motion-track ver 0.7 written by Claude Pageau pageauc@gmail.com
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
dependencies

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-opencv python-picamera
sudo apt-get install libgl1-mesa-dri  

"""
print("%s %s using python2 and OpenCV2" % (progname, ver))
print("Loading Please Wait ....")
import io
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np

debug = True        # Set to False for no data display
window_on = False   # Set to True displays opencv windows (GUI desktop reqd)
SHOW_CIRCLE = True  # show a circle otherwise show bounding rectancle on window
CIRCLE_SIZE = 10    # diameter of circle to show motion location in window
LINE_THICKNESS = 1  # thicknes of bounding line in pixels
WINDOW_BIGGER = 1   # resize multiplier for speed photo image and if gui_window_on=True then makes opencv window bigger
                    # Note if the window is larger than 1 then a reduced frame rate will occur

# Camera Settings
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CAMERA_HFLIP = False
CAMERA_VFLIP = True
CAMERA_FRAMERATE = 15

# Motion Tracking Settings
THRESHOLD_SENSITIVITY = 25
BLUR_SIZE = 10
MIN_AREA = 25       # excludes all contours less than or equal to this Area

def show_FPS(start_time,frame_count):
    if debug:
        if frame_count >= 10:
            duration = float(time.time() - start_time)
            FPS = float(frame_count / duration)
            print("Processing at %.2f fps last %i frames" %( FPS, frame_count))
            frame_count = 0
            start_time = time.time()
        else:
            frame_count += 1
    return start_time, frame_count

def motion_track():
    print("Initializing Camera ....")
    # Save images to an in-program stream
    camera = PiCamera()
    camera.hflip = CAMERA_HFLIP
    camera.vflip = CAMERA_VFLIP          
    camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
    camera.framerate = CAMERA_FRAMERATE
    rawCapture = PiRGBArray(camera, size=(CAMERA_WIDTH, CAMERA_HEIGHT))
    time.sleep(1)
    first_image = True
    if window_on:
        print("press q to quit opencv display")
    else:
        print("press ctrl-c to quit")        
    print("Start Motion Tracking ....")
    frame_count = 0
    start_time = time.time()
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image2 = frame.array        
        start_time, frame_count = show_FPS(start_time, frame_count)
        # initialize variables         
        motion_found = False
        biggest_area = MIN_AREA
        cx = 0
        cy = 0
        cw = 0
        ch = 0
        # At this point the image is available as stream.array
        if first_image:
            # initialize image1 using image2 (only done first time)
            image1 = image2
            grayimage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            first_image = False
        else:
            # Convert to gray scale, which is easier
            grayimage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            # Get differences between the two greyed, blurred images
            differenceimage = cv2.absdiff(grayimage1, grayimage2)
            differenceimage = cv2.blur(differenceimage,(BLUR_SIZE,BLUR_SIZE))
            # Get threshold of difference image based on THRESHOLD_SENSITIVITY variable
            retval, thresholdimage = cv2.threshold(differenceimage,THRESHOLD_SENSITIVITY,255,cv2.THRESH_BINARY)
            # Get all the contours found in the thresholdimage
            contours, hierarchy = cv2.findContours(thresholdimage,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            total_contours = len(contours)
            # save grayimage2 to grayimage1 ready for next image2
            grayimage1 = grayimage2
            # find contour with biggest area
            for c in contours:
                # get area of next contour
                found_area = cv2.contourArea(c)
                # find the middle of largest bounding rectangle
                if found_area > biggest_area:
                    motion_found = True
                    biggest_area = found_area
                    (x, y, w, h) = cv2.boundingRect(c)
                    cx = int(x + w/2)   # put circle in middle of width
                    cy = int(y + h/6)   # put circle closer to top
                    cw = w
                    ch = h
            if motion_found:
                # Do Something here with motion data
                if window_on:
                    # show small circle at motion location
                    if SHOW_CIRCLE:
                        cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,255,0), LINE_THICKNESS)
                    else:
                        cv2.rectangle(image2,(cx,cy),(x+cw,y+ch),(0,255,0), LINE_THICKNESS)                  
                if debug:
                    print("total_Contours=%2i  Motion at cx=%3i cy=%3i   biggest_area:%3ix%3i=%5i" % (total_contours, cx ,cy, cw, ch, biggest_area))
            if window_on:
                # cv2.imshow('Difference Image',differenceimage) 
                cv2.imshow('Threshold Image', thresholdimage)
                if WINDOW_BIGGER > 1:  # Note setting a bigger window will slow the FPS
                    big_w = CAMERA_WIDTH * WINDOW_BIGGER
                    big_h = CAMERA_HEIGHT * WINDOW_BIGGER
                    image2 = cv2.resize( image2,( big_w, big_h ))                             
                cv2.imshow('Movement Status', image2)
                # Close Window if q pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    print("End Motion Tracking")
                    break
        rawCapture.truncate(0)
#-----------------------------------------------------------------------------------------------    
if __name__ == '__main__':
    try:
        motion_track()
    finally:
        print("")
        print("+++++++++++++++++++++++++++++++++++")
        print("%s %s - Exiting" % (progname, ver))
        print("+++++++++++++++++++++++++++++++++++")
        print("")                                



