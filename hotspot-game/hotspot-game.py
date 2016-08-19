#!/usr/bin/env python

"""
hotspot-game ver 0.8 written by Claude Pageau pageauc@gmail.com
Raspberry (Pi) - python opencv2 motion tracking using picamera module

This is a raspberry pi python opencv2 motion tracking demonstration game.
It will detect motion in the field of view and return x and y coordinates
of the most dominant contour.  Keep your body still and move your hand
to activate menu's and hit the hotspot box to score points.  The High
score is saved in a file.

Some of this code is base on a YouTube tutorial by
Kyle Hounslow using C here https://www.youtube.com/watch?v=X6rPdRZzgjg

Here is my YouTube video demonstrating motion tracking using a 
Raspberry Pi B2 https://youtu.be/09JS7twPBsQ

Requires a Raspberry Pi with a RPI camera module installed and configured
dependencies

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-opencv python-picamera

"""
progname = "hotspot_game.py ver 0.8"
print("%s using python2 and OpenCV2" % (progname))
print("Loading Please Wait ....")

import os
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import numpy as np
from threading import Thread
from random import randint

# Display Settings
window_on = True       # Set to True displays opencv windows (GUI desktop reqd)
WINDOW_BIGGER = 1.5    # resize multiplier if window_on=True then makes opencv window bigger
debug = True           # Set to False for no data display

# Game Settings
hi_score_path = "hotspot_hi_score"

# Game Timers
target_timer = 4    # seconds to show target rectangle on screen before moving it

# Game Settings
hotspot_skill = 150  # starting size of rectangle in pixels
hotspot_max_levels = 10   # default=10 Number of game levels lasting hotspot_level_timer 
hotspot_level_timer = 10  # seconds of time on each level
hotspot_min_size = int( hotspot_skill / 8 )

# Camera Settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_HFLIP = False
CAMERA_VFLIP = True
CAMERA_ROTATION = 0
CAMERA_FRAMERATE = 45

# Menu Settings
MENU_COUNTER = 12     # number of motions inside menu for selection
MENU_WIDTH = 200
MENU_HEIGHT = 75
MENU_LINE_WIDTH = 2

# Motion Tracking Settings
THRESHOLD_SENSITIVITY = 25
BLUR_SIZE = 10
MIN_AREA = 600      # excludes all contours less than or equal to this Area
CIRCLE_SIZE = 8      # diameter of circle to show motion location in window
CIRCLE_LINE = 3      # thickness of line for circle
FONT_SCALE = .5      # OpenCV window text font size scaling factor default=.5 (lower is smaller)
LINE_THICKNESS = 2   # thickness of bounding line in pixels
big_w = int(CAMERA_WIDTH * WINDOW_BIGGER)
big_h = int(CAMERA_HEIGHT * WINDOW_BIGGER)

#-----------------------------------------------------------------------------------------------  
class PiVideoStream:    # Video Stream using Treading
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
def read_hiscore(hi_score_path, hi_score):
    if not os.path.exists(hi_score_path):
        open(hi_score_path, 'w').close()
        f = open(hi_score_path, 'w+')
        f.write(str(hi_score))
        f.close()
    with open(hi_score_path, 'r') as f:
        hi_score = f.read()
        f.closed
        hi_score = int(hi_score)
    return hi_score

#-----------------------------------------------------------------------------------------------    
def save_hiscore(hi_score_path, hi_score):
    if not os.path.exists(hi_score_path):
        open(hi_score_path, 'w').close()
    f = open(hi_score_path, 'w+')
    f.write(str(hi_score))
    f.close()
        
#-----------------------------------------------------------------------------------------------
def check_for_hit(x,y):
    global hsx
    global hsy
    global hotspot_size
    got_hit = False
    # procedure for processing motion location data
    if ( x < hsx + hotspot_size and x > hsx - hotspot_size and
         y < hsy + hotspot_size and y > hsy - hotspot_size):
        got_hit = True
    return got_hit
    
#-----------------------------------------------------------------------------------------------  
def hotspot_game():
    print("Initializing Camera ....")  
    # Setup video stream on a processor Thread for faster speed
    vs = PiVideoStream().start()
    vs.camera.rotation = CAMERA_ROTATION
    vs.camera.hflip = CAMERA_HFLIP
    vs.camera.vflip = CAMERA_VFLIP
    time.sleep(2.0)    # Give Camera time to initialize

    # initialize Variables
    global hsx
    global hsy
    global hotspot_size
    level_timer = hotspot_level_timer
    hsx = randint(10, CAMERA_WIDTH - int(CAMERA_WIDTH/8)) 
    hsy = randint(10, CAMERA_HEIGHT - int(CAMERA_HEIGHT/8))

    target_start = time.time()
    level_start_time = time.time() 
    
    hotspot_hiscore = 0
    hotspot_hiscore = read_hiscore(hi_score_path, hotspot_hiscore)    
    hotspot_size = hotspot_skill
    hotspot_score = 0
    hotspot_level = 1
    player = "PLAYER  "
    
    # menu hitcounters
    player1_hitcount = 0
    player2_hitcount = 0
    play_hitcount = 0
    quit_hitcount = 0
    
    end_of_game = False
    motion_found = False
    found_hit = False
    ready_counter = 4
    
    # Game Section indicators
    begingame = True
    readyplayer = False
    playgame = False
    endgame = False
    
    # Initialize first image as stream.array   
    image2 = vs.read() 
    grayimage1 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    while not end_of_game:
        # initialize variables               
        image2 = vs.read()  # Initialize second image   
        # Convert image to gray scale for start of motion tracking
        grayimage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        # Get differences between the two greyed, blurred images
        differenceimage = cv2.absdiff(grayimage1, grayimage2)
        grayimage1 = grayimage2   # Update grayimage1 for next iteration
        differenceimage = cv2.blur(differenceimage,(BLUR_SIZE,BLUR_SIZE))
        # Get threshold of difference image based on THRESHOLD_SENSITIVITY variable
        retval, thresholdimage = cv2.threshold(differenceimage,THRESHOLD_SENSITIVITY,255,cv2.THRESH_BINARY)
        # Get all the contours found in the thresholdimage
        contours, hierarchy = cv2.findContours(thresholdimage,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        total_contours = len(contours)

        if playgame:
            biggest_area = MIN_AREA
        else:
            biggest_area = 4000        

        motion_found = False
        cx = -1
        cy = -1
        cw = -1
        ch = -1
        found_area = 0   
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
                cy = y + h/2   # put circle closer to top
                cw = w
                ch = h
        
        if window_on:
            if begingame:   # Pick Players 
               # Display Player Choice Menu
                player1_x = int(CAMERA_WIDTH/6)
                player1_y = 200
                cv2.rectangle(image2, (player1_x, player1_y), (player1_x+ MENU_WIDTH, player1_y+ MENU_HEIGHT), (0,255,0), MENU_LINE_WIDTH)
                cv2.putText(image2, "PLAYER 1", ( player1_x + int(MENU_WIDTH/3), int( player1_y + MENU_HEIGHT/2)),
                                                  cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE , (0,255,0), MENU_LINE_WIDTH)
                # Display Quit Menu
                player2_x = player1_x + MENU_WIDTH + 20
                player2_y = 200
                cv2.rectangle(image2, (player2_x, player2_y), (player2_x+ MENU_WIDTH, player2_y+ MENU_HEIGHT), (0,255,0), MENU_LINE_WIDTH)
                cv2.putText(image2, "PLAYER 2", ( player2_x + int(MENU_WIDTH/3), int( player2_y + MENU_HEIGHT/2)),
                                                  cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE , (0,255,0), MENU_LINE_WIDTH) 
 
                # Player 1 Menu Box
                if (cx > player1_x and cx < player1_x + MENU_WIDTH and cy > player1_y and cy < player1_y + MENU_HEIGHT):
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,0,255),CIRCLE_LINE) 
                    player1_hitcount += 1
                    player2_hitcount = 0                    
                    if player1_hitcount > MENU_COUNTER: 
                        player = "PLAYER 1"
                        player1_hitcount = 0
                        player2_hitcount = 0
                        begingame = False
                        endgame = False
                        playgame = False
                        readyplayer = True
                        ready_counter = 4
                # Player 2 Menu Box
                elif (cx > player2_x and cx < player2_x + MENU_WIDTH and cy > player2_y and cy < player2_y + MENU_HEIGHT):
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,0,255),CIRCLE_LINE) 
                    player2_hitcount += 1
                    player1_hitcount = 0                    
                    if player2_hitcount > MENU_COUNTER: 
                        player = "PLAYER 2"
                        player1_hitcount = 0
                        player2_hitcount = 0
                        begingame = False
                        endgame = False
                        playgame = False
                        readyplayer = True
                        ready_counter = 4
                else:
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,255, 0),CIRCLE_LINE)
                    
            elif readyplayer:   # Player Count Down to Start Playing
                ready_counter = ready_counter - 1
                if ready_counter < 0:
                    ready_counter = 4
                    readyplayer = False
                    endgame = False
                    playgame = True               
        
            elif playgame:      # Main Hotspot Game                       
                if time.time() - level_start_time > level_timer:
                    level_start_time = time.time()
                    
                    if hotspot_level < hotspot_max_levels:
                        hotspot_level += 1
                    else:
                        hotspot_level = hotspot_max_levels
                        begingame = False                        
                        playgame = False
                        endgame = True
                        
                    if hotspot_size < hotspot_min_size:
                        hotspot_size = hotspot_min_size
                    else:
                        hotspot_size = hotspot_size - int(hotspot_skill/ hotspot_max_levels)   

                if motion_found:
                    found_hit = check_for_hit(cx,cy)
                # show small circle at motion location                   
                if found_hit:
                    hotspot_score += 5   # Update Score
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,0,255),CIRCLE_LINE)
                    cv2.rectangle(image2,(hsx, hsy), (hsx + hotspot_size, hsy + hotspot_size), (0,0,255),LINE_THICKNESS +1)                   
                else:
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,255,0),CIRCLE_LINE) 
                    cv2.rectangle(image2,(hsx, hsy), (hsx + hotspot_size, hsy + hotspot_size), (0,255,0),LINE_THICKNESS)                   
                    
                # display a target square for hotspot game if selected                            
                target_diff = time.time() - target_start
                if target_diff > target_timer:
                    hsx = randint(int(CAMERA_WIDTH/8), CAMERA_WIDTH - int(CAMERA_WIDTH/8)) 
                    hsy = randint(int(CAMERA_HEIGHT/8), CAMERA_HEIGHT - int(CAMERA_HEIGHT/8))                                
                    target_start = time.time()
                
            elif endgame:      # Game result display and Play, Quit Menu                 
                # Game Over ask to play again.
                play_x = int(CAMERA_WIDTH/6)
                play_y = 200              
                
                if hotspot_score > hotspot_hiscore:
                    m_text = "GAME OVER .. NEW HI SCORE %i"  % ( hotspot_score )
                    save_hiscore(hi_score_path, hotspot_score)
                else:                    
                    m_text = "GAME OVER .. YOUR SCORE %i"  % ( hotspot_score )
                cv2.putText(image2, m_text, ( play_x, int(CAMERA_HEIGHT/3)), cv2.FONT_HERSHEY_SIMPLEX, .75 , (0,0,255), 2)
                
                # Display Play and Quit Menu Choices
                # Play Again Menu Box
                cv2.rectangle(image2, (play_x, play_y), (play_x+ MENU_WIDTH, play_y+ MENU_HEIGHT), (0,255,0), MENU_LINE_WIDTH)
                cv2.putText(image2, "PLAY AGAIN ?", ( play_x + int(MENU_WIDTH/3), int( play_y + MENU_HEIGHT/2)),
                                                      cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE , (0,255,0), MENU_LINE_WIDTH)
                # Display Quit Menu Box
                quit_x = play_x + MENU_WIDTH + 20
                quit_y = 200
                cv2.rectangle(image2, (quit_x, quit_y), (quit_x+ MENU_WIDTH, quit_y+ MENU_HEIGHT), (0,255,0), MENU_LINE_WIDTH)
                cv2.putText(image2, "QUIT", ( quit_x + int(MENU_WIDTH/3), int( quit_y + MENU_HEIGHT/2)), 
                                              cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE , (0,255,0), MENU_LINE_WIDTH) 
 
                # Play Again Menu Box
                if (cx > play_x and cx < play_x + MENU_WIDTH and cy > play_y and cy < play_y + MENU_HEIGHT):
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,0,255),CIRCLE_LINE) 
                    play_hitcount += 1
                    quit_hitcount = 0                    
                    if play_hitcount > MENU_COUNTER: 
                        play_hitcount = 0
                        quit_hitcount = 0                  
                        hotspot_size = hotspot_skill
                        if hotspot_score > hotspot_hiscore:
                            hotspot_hiscore = hotspot_score                      
                        hotspot_score = 0
                        hotspot_level = 1
                        end_of_game = False                     
                        playgame = False
                        endgame = False
                        readyplayer = False
                        begingame = True

                        
                # Quit Menu Box
                elif (cx > quit_x and cx < quit_x + MENU_WIDTH and cy > quit_y and cy < quit_y + MENU_HEIGHT):
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,0,255),CIRCLE_LINE) 
                    quit_hitcount += 1
                    play_hitcount = 0                    
                    if quit_hitcount > MENU_COUNTER: 
                        playgame = False
                        begingame = False
                        end_of_game = True
                else:
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,255, 0),CIRCLE_LINE)                 

            if readyplayer:  # Display Player Count Down to Start New Game
                time.sleep(1.5) 
                cv2.putText(image2, "READY " + player, ( 200, int( player2_y + MENU_HEIGHT/2)),
                            cv2.FONT_HERSHEY_SIMPLEX, .75 , (0,0,255), MENU_LINE_WIDTH)      
                cv2.putText(image2, str(ready_counter) , ( 300, int( player2_y + MENU_HEIGHT/2) + 40),
                            cv2.FONT_HERSHEY_SIMPLEX, .75 , (0,0,255), MENU_LINE_WIDTH)

            else:   # Display Game Information at top of Screen
                 m_text = "%s SCORE %i  LEVEL %i  HI SCORE %i  "  % ( player, hotspot_score, hotspot_level, hotspot_hiscore)
                 cv2.putText(image2, m_text, ( 2, 20), cv2.FONT_HERSHEY_SIMPLEX, .75 , (0,255,0), 2)       
                
            if WINDOW_BIGGER > 1:
                # resize motion window to desired size
                image2 = cv2.resize(image2, (big_w, big_h))
                cv2.imshow('HOTSPOT GAME q in Window to Quit', image2)  # bigger size                        
            else:
                # display original image size motion window 
                cv2.imshow('HOTSPOT BAME q in Window to Quit', image2) # original size
                # cv2.imshow('Threshold Image', thresholdimage)
                # cv2.imshow('Difference Image',differenceimage           
                      
            if cv2.waitKey(1) & 0xFF == ord('q'):   # Close Window if q pressed   
                cv2.destroyAllWindows()
                print("")
                print("ctrl-q pressed End %s"  % (progname))
                vs.stop() 
                end_of_game = True
            
        if debug:
            if motion_found:
                print("total_Contours=%2i  Motion at cx=%3i cy=%3i  Area:%3ix%3i=%5i" % (total_contours, cx ,cy, cw, ch, cw*ch))                      
                 
 #-----------------------------------------------------------------------------------------------    
if __name__ == '__main__':
    try:
        hotspot_game()
    finally:
        print("")
        print("+++++++++++++++++++++++++++++++++++")
        print("%s - Exiting Program" % progname)
        print("+++++++++++++++++++++++++++++++++++")
        print("")               


