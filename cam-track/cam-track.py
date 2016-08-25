#!/usr/bin/env python

progname = "cam-track.py"
ver = "version 0.71"

"""
cam-track ver 0.71 written by Claude Pageau pageauc@gmail.com
Raspberry (Pi) - python opencv2 camera pan/tilt tracking using picamera module

This is a raspberry pi python opencv2 camera tracking demonstration program.
It takes a sample search rectangle from center of video stream image
and tracks its position based on a percent accuracy at sw_maxLoc.
As the camera pans and tilts.  The cumulative position is displayed.

I will work ant converting position based on 360 degrees camera movement.
This is still very much a work in progress but I thought it would be
useful for others who might want a simple way to track camera movement.
Note the program can get confused by plain surroundings or some
other movements in the frame although this can be tuned out somewhat
using the 
sw_maxLoc - This is how closely the search rect matches inside the image
sw_minVal - This is the lowest value match in the image.

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
import io
import time
import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from operator import itemgetter
import numpy as np

#-----------------------------------------------------------------------------------------------  
# Global Variable Settings
debug = True          # Set to False for no data display
window_on = True      # Set to True displays opencv windows (GUI desktop reqd)
fps_on = False        # Display fps (not implemented)

# OpenCV Settings
WINDOW_BIGGER = 2.0   # increase the display window size
MAX_SEARCH_THRESHOLD = .97  # default=.97 Accuracy for best search result of search_rect in stream images
MIN_SEARCH_THRESHOLD = .45  # default=.45 Accuracy for worst search result of search rect in stream images
LINE_THICKNESS = 1    # thickness of bounding line in pixels
CV_FONT_SIZE = .25    # size of font on opencv window default .5
# SHOW_CIRCLE = True  # show a circle otherwise show bounding rectancle on window
# CIRCLE_SIZE = 8     # diameter of circle to show motion location in window

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

#-----------------------------------------------------------------------------------------------  
# Currently not used but included in case you want to check speed
def show_FPS(start_time,frame_count):
    if debug:
        if frame_count >= FRAME_COUNTER:
            duration = float(time.time() - start_time)
            FPS = float(frame_count / duration)
            print("Processing at %.2f fps last %i frames" %( FPS, frame_count))
            frame_count = 0
            start_time = time.time()
        else:
            frame_count += 1
    return start_time, frame_count

#-----------------------------------------------------------------------------------------------     
def get_center(x,y,w,h):
    return int(x+w/2), int(y+h/2)    
    
#-----------------------------------------------------------------------------------------------  
def cam_shift():
    # Process steam images to find camera movement 
    # using an extracted search rectangle in the middle of one frame
    # and find location in subsequent images.  Grap a new search rect
    # as needed based on nearness to edge of image or percent probability
    # of image search result Etc.
    
    # Setup Video Stream Thread
    vs = PiVideoStream().start()
    vs.camera.rotation = CAMERA_ROTATION
    vs.camera.hflip = CAMERA_HFLIP
    vs.camera.vflip = CAMERA_VFLIP
    time.sleep(2.0)    
      
    # initialize the search window (rect) variables 
    if WINDOW_BIGGER > 1:  # Note setting a bigger window will slow the FPS
        big_w = int(CAMERA_WIDTH * WINDOW_BIGGER)
        big_h = int(CAMERA_HEIGHT * WINDOW_BIGGER) 
    sw_w = int(CAMERA_WIDTH/4)    # search window width
    sw_h = int(CAMERA_HEIGHT/4)   # search window height
    sw_buf_x = int(sw_w/4)        # buffer to left/right of image
    sw_buf_y = int(sw_h/4)        # buffer to top/bot of image
    sw_cx = int(CAMERA_WIDTH/2)   # x center of image
    sw_cy = int(CAMERA_HEIGHT/2)  # y center of image   
    sw_x = (sw_cx - sw_w/2)       # top x corner of search rect
    sw_y = (sw_cy - sw_h/2)       # top y corner of search rect
    sw_maxVal = MAX_SEARCH_THRESHOLD  # Threshold Accuracy of search in image
    sw_minVal = MIN_SEARCH_THRESHOLD  # Threshold of worst search result in image
    
    # Grab a Video Steam image and initialize search rectangle
    cam_cx1 = sw_cx
    cam_cy1 = sw_cy
    cam_cur_cx = cam_cx1
    cam_cur_cy = cam_cy1
    image1 = vs.read()   # initialize first image
    search_rect = image1[sw_y:sw_y+sw_h, sw_x:sw_x+sw_w]  # Initialize centre search rectangle
    cam_track_cx = 0   # initialize cam horizontal cam movement tracker
    cam_track_cy = 0   # initialize cam vertical cam movement tracker
    while True:
        image1 = vs.read()  # capture a image from video stream thread
        # Look for search_rect in this image and return result
        result = cv2.matchTemplate( image1, search_rect, cv2.TM_CCORR_NORMED)
        # Process result to return probabilities and Location of best and worst image match
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)  # find search rect match in new image
        # Get the center of the best matching result of search
        cam_cx2, cam_cy2 = get_center( maxLoc[0], maxLoc[1], sw_w, sw_h ) 
        # Update cumulative camera tracking data        
        cam_track_cx = cam_track_cx + cam_cur_cx - cam_cx2
        cam_track_cy = cam_track_cy + cam_cur_cy - cam_cy2 
        # Check if search rect is near edges and meets search accuracy threshold
        if not ( maxLoc[0] > sw_buf_x and maxLoc[0] + sw_x + sw_buf_x < CAMERA_WIDTH and
                 maxLoc[1] > sw_buf_y and maxLoc[1] + sw_y + sw_buf_y < CAMERA_HEIGHT
                 and maxVal > sw_maxVal):
            # check value of lowest matching result and reset search rectangle
            if minVal < sw_minVal:             
                if debug:
                    print("    Reset search_rect cur_cx=%i cam_track_cx=%i cur_cy=%i cam_track_cy=%i" 
                    % (cam_cur_cx, cam_track_cx, cam_cur_cy, cam_track_cy))        
                search_rect = image1[sw_y:sw_y+sw_h, sw_x:sw_x+sw_w]
                
                cam_cx2, cam_cy2 = get_center( maxLoc[0], maxLoc[1], sw_w, sw_h )   
                cam_track_cx = cam_track_cx + cam_cur_cx - cam_cx2
                cam_track_cy = cam_track_cy + cam_cur_cy - cam_cy2 
                cam_cx1 = sw_cx
                cam_cy1 = sw_cy
                cam_cx2 = cam_cx1
                cam_cy2 = cam_cy1
        cam_cur_cx = cam_cx2
        cam_cur_cy = cam_cy2 
        
        if debug: 
            print(" Cam at (%i,%i) cam_track_cx, cam_track_cy" % ( cam_track_cx, cam_track_cy, ))
            print(" maxLoc   maxVal   minLoc   minVal")
            print maxLoc, "{0:0.4f}".format(maxVal) ,  minLoc ,"{0:0.4f}".format(minVal) 
        image2 = image1
           
        if window_on:
            # Display openCV window information on RPI desktop if required
            cv2.imshow( 'search rectangle', search_rect ) 
            #  cv2.circle(image2,(sw_x+sw_w/2,sw_y+sw_h/2),CIRCLE_SIZE,(0,0,255), 2) 
            #  cv2.rectangle(image2,(sw_x,sw_y),(sw_x+sw_w,sw_y+sw_h),(0,0,255), LINE_THICKNESS)         
            cv2.rectangle(image2,( maxLoc[0], maxLoc[1] ),( maxLoc[0] + sw_w, maxLoc[1] + sw_h ),(0,255,0), LINE_THICKNESS)     # show search rect
            # cv2.rectangle(image2,( cam_cx1 - sw_w/2, cam_cy2 - sw_h/2 ),(cam_cx1+sw_w/2, cam_cy2+sw_h/2),(0,0,255), LINE_THICKNESS) # show current rect
            m_text = ("CAM POS ( %i %i )   " % (cam_track_cx, cam_track_cy))
            cv2.putText(image2, m_text, (int(CAMERA_WIDTH/2) - len(m_text) * 3, CAMERA_HEIGHT - 30 ), cv2.FONT_HERSHEY_SIMPLEX, CV_FONT_SIZE, (255,255,255), 1)
            if WINDOW_BIGGER > 1:
                image2 = cv2.resize( image2,( big_w, big_h ))             

            cv2.imshow('Cam-Track  (q in window to quit)',image2)     

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                print("End Cam Tracking")
                break
     
#-----------------------------------------------------------------------------------------------    
if __name__ == '__main__':
    try:
        cam_shift()
    finally:
        print("")
        print("+++++++++++++++++++++++++++++++++++")
        print("%s %s - Exiting" % (progname, ver))
        print("+++++++++++++++++++++++++++++++++++")
        print("")                                



