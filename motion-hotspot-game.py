#!/usr/bin/env python

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

"""
print("motion-track.py using python2 and OpenCV2")
print("Loading Please Wait ....")
import io
import time
#import datetime
import picamera
import picamera.array
import cv2
import numpy as np

debug = True       # Set False for no terminal data display
window_on = False  # Set True to display opencv windows (GUI desktop Reqd)
hotspot_game = True
hotspot_skill = 40

# Camera Settings
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CAMERA_HFLIP = False
CAMERA_VFLIP = False

# Motion Tracking Settings
THRESHOLD_SENSITIVITY = 25
BLUR_SIZE = 10
MIN_AREA = 25     # excludes all contours less than or equal to this Area
CIRCLE_SIZE = 10  # diameter of circle to show motion location in window

# Resize GUI desktop motion window for better viewing. False is default camera image size
bigwindow_on = True
big_w = CAMERA_WIDTH * 3      # x2=640 x3=960
big_h = CAMERA_HEIGHT * 3     # x2=480 x3=720

#-----------------------------------------------------------------------------------------------
def motion_game(x,y):
    if hotspot_game: 
        hold_position = False
        #Empty procedure for processing motion location data
        if x < (CAMERA_WIDTH/2) - hotspot_skill:
            print("<--- LEFT")
        elif x > (CAMERA_WIDTH/2) + hotspot_skill:
            print("RIGHT -->")
        elif y < (CAMERA_HEIGHT/2) - hotspot_skill:    
            print(" DOWN V")
        elif y > (CAMERA_HEIGHT/2) + hotspot_skill:
            print("  UP !")
        else:
            hold_position = True
        return hold_position
        
#-----------------------------------------------------------------------------------------------
def show_fps(start_time,frame_count):
    if debug and not hotspot_game:
        duration = float(time.time() - start_time)
        if duration > 10.0:
            FPS = float(frame_count / duration)
            print("Processing at %.2f fps  %i frames in %0.2f sec" %( FPS, frame_count, duration))
            frame_count = 0
            start_time = time.time()
        frame_count += 1
    return start_time, frame_count

#-----------------------------------------------------------------------------------------------  
def motion_track():
    print("Initializing Camera ....")
    # Save images to an in-program stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
        camera.hflip = CAMERA_HFLIP
        camera.vflip = CAMERA_VFLIP      
        time.sleep(2)
        first_image = True
        if window_on:
            print("press q to quit opencv display")
        else:
            print("set variable window_on=True for GUI window on desktop")
            print("press ctrl-c to quit")        
        print("Start Motion Tracking ....")
        if hotspot_game:
            hotspot_level = hotspot_skill
            hotspot_highscore = 0
            print("hotspot_game=%s" % hotspot_game)
            print("##########################################")
            print("##      Play Find the Hotspot           ##")
            print("##  Find It and Move a Little to Score  ##")
            print("##########################################")
            print("HIGHSCORE %i at SKILL %i" % (hotspot_highscore, hotspot_skill))
            print("START GAME in 5 SECONDS")
            time.sleep(5)
            print("GET READY ...")
        frame_count = 0
        start_time = time.time()
        game_count = 0
        hotspot_level = hotspot_skill
        while(True):
            start_time, frame_count = show_fps(start_time, frame_count)
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
                        in_center = motion_game(cx,cy)
                        if in_center and hotspot_game:
                            game_count += 1
                            countdown = 4 - game_count
                            if game_count > 4:
                                print("################")
                                print("##  SUCCESS   ##")
                                print("################")
                                hotspot_highscore += 5                                
                                print("HIGHSCORE %i at SKILL %i" % (hotspot_highscore, hotspot_level))
                                hotspot_level = hotspot_level - 5
                                if hotspot_level < 10:
                                    print("Thanks for Playing ... Bye")
                                    break
                                print("")
                                print("NEXT LEVEL in 5 SECONDS")
                                time.sleep(5)
                                print("GET READY ...")
                                time.sleep(1)
                                game_count = 0
                            if game_count > 0:
                                print("HOTSPOT Wait ... %i" % countdown)                    
                        else:
                            if hotspot_game:
                                game_count = 0           
                        if window_on:
                            # show small circle at motion location
                            cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,255,0),2)
                            # display a target square for hotspot game if selected                            
                            if hotspot_game:
                                hsx = (CAMERA_WIDTH / 2) - (hotspot_level / 2)
                                hsy = (CAMERA_HEIGHT / 2) - (hotspot_level / 2)                                
                                cv2.rectangle(image2,(hsx, hsy), (hsx + hotspot_level, hsy + hotspot_level), (0,255,0),2)                            
                        if debug and not hotspot_game:
                            print("total_Contours=%2i  Motion at cx=%3i cy=%3i  Area:%3ix%3i=%5i" % (total_contours, cx ,cy, cw, ch, biggest_area))
                    
                    if window_on:
                        if bigwindow_on:
                            # resize motion window to desired size
                            image3 = cv2.resize(image2,(big_w, big_h))
                            cv2.imshow('Movement Status', image3)                          
                        else:
                            # display original image size motion window 
                            cv2.imshow('Movement Status', image2)
                            cv2.imshow('Threshold Image', thresholdimage)
                            # cv2.imshow('Difference Image',differenceimage)
                        # Close Window if q pressed
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            cv2.destroyAllWindows()
                            print("End Motion Tracking")
                            break

motion_track()

