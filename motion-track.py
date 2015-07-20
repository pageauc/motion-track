#!/usr/bin/env python

"""
motion-track ver 0.6 written by Claude Pageau pageauc@gmail.com
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

"""
print("Loading Please Wait ....")
import io
import time
#import datetime
import picamera
import picamera.array
import cv2
import numpy as np

debug = True      # Set to False for no data display
window_on = True  # Set to True displays opencv windows (GUI desktop reqd)

# Camera Settings
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CAMERA_HFLIP = True
CAMERA_VFLIP = False

# Motion Tracking Settings
THRESHOLD_SENSITIVITY = 25
BLUR_SIZE = 10
MIN_AREA = 25    # excludes all contours less than or equal to this Area

def motion_track():
    print("Initializing Camera ...")
    # Save images to an in-program stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
        camera.hflip = CAMERA_HFLIP
        camera.vflip = CAMERA_VFLIP      
        time.sleep(2)
        first_image = True
        print("Start Motion Tracking ....")
        if window_on:
            print("press q to quit opencv display")
        else:
            print("press ctrl-c to quit")        
        while(True):
            # initialize variables         
            motion_found = False
            biggest_area = MIN_AREA
            cx = 0
            cy = 0
            cw = 0
            ch = 0
            with picamera.array.PiRGBArray(camera) as stream:
                camera.capture(stream, format='bgr')
                image2 = stream.array
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
                            cx = x + w/2   # put circle in middle of width
                            cy = y + h/6   # put circle closer to top
                            cw = w
                            ch = h
                    if motion_found:
                        # Do Something here with motion data
                        if debug:                
                            cv2.circle(image2,(cx,cy),10,(0,255,0),2)
                            print("total_Contours=%2i  Motion at cx=%3i cy=%3i   biggest_area:%3ix%3i=%5i" % (total_contours, cx ,cy, cw, ch, biggest_area))
                    else:
                        if debug:                
                            print("total_contours=%2i  No Motion" % (total_contours))                    
                    if window_on:
                        # cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        # cv2.imshow('Difference Image',differenceimage) 
                        cv2.imshow('Threshold Image', thresholdimage)
                        cv2.imshow('Movement Status', image2)
                        # Close Window if q pressed
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            cv2.destroyAllWindows()
                            print("End Motion Tracking")
                            break

motion_track()

