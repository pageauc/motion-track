#!/usr/bin/env python

"""
motion-track ver 0.5 written by Claude Pageau pageauc@gmail.com
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
Raspberry Pi B2 http://youtu.be/09JS7twPBsQ

Requires a Raspberry Pi with a RPI camera module installed and configured
dependencies

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-opencv python-picamera

"""

import io
import time
import picamera
import picamera.array
import cv2
import numpy as np

debug = True   # set to True and launch from a gui desktop with attached monitor
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CAMERA_HFLIP = True
CAMERA_VFLIP = False

# You can adjust these opencv2 settings if you like.
THRESHOLD_SENSITIVITY = 25  
BLUR_SIZE = 10

#------------------------------------------------------------------------------
def motion_track():
    # Save images to an in-program stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
        camera.hflip = CAMERA_HFLIP
        camera.vflip = CAMERA_VFLIP
        time.sleep(2)
        first_image = True
        while(True):
            with picamera.array.PiRGBArray(camera) as stream:
                camera.capture(stream, format='bgr')
                image2 = stream.array
                # At this point the image is available as stream.array
                if first_image:
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
                    # save grayimage2 to grayimage1 ready for next image2
                    grayimage1 = grayimage2  # prepare for next image2
                    if debug:
                        print("Total Contours %i" % len(contours))
                    # initialize variables
                    biggestArea = 0
                    cx = 0
                    cy = 0
                    # find contour with biggest area
                    for c in contours:
                        # get area of next contour
                        foundArea = cv2.contourArea(c)
                        # find the middle of largest bounding rectangle
                        if foundArea > biggestArea:
                            biggestArea = foundArea
                            (x, y, w, h) = cv2.boundingRect(c)
                            cx = x + w/2   # put circle in middle of width
                            cy = y + h/6   # put circle closer to top                          
                    if biggestArea > 0:
                        if debug:
                            print("Movement Found at cx=%i cy=%i area=%i" % (cx ,cy, biggestArea))
                            # cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.circle(image2,(cx,cy),10,(0,255,0),2)
                    if debug: 
                        # cv2.imshow('Difference Image',differenceimage) 
                        cv2.imshow('Threshold Image', thresholdimage)
                        cv2.imshow('Movement Status', image2)
            if debug:
                # Close Window
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

motion_track()

