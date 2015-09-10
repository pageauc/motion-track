#                          speed_track.py

###               A Raspberry Pi vehicle speed camera
##### using a Raspberry Pi computer, python, openCV and picamera module
#####          written by Claude Pageau pageauc@gmail.com

###Version .97 Release 9-Sep-2015
* Changed Calibration to detect motion and take photo automatically
  They are now saved in images folder with prefix calib-
* Changed speed photo to use resized existing motion image instead of 
  a New large image
* Added speed to speed photo filename to allow sorting by speed.
* Final image is from previous event rather than current event to
  have motion more in view.
* Improved verbose logging
* Improved CSV log to put hour and minutes in separate columns.
  This allows for using as pivot table in spreatsheet 

### Program Description
This is a raspberry pi computer openCV vehicle speed camera demo program.
It is written in python and uses openCV2 to detect and track object motion.
The results are recorded on speed photos and in a CSV log file that can be
imported to another program for additiona processing.  
The program will detect motion in the field of view and use opencv to calculate
the largest contour and return its x,y coordinate. Motion detection is
restricted between y_upper and y_lower variables (road area).  If a track
is longer than track_len_trig variable then average speed will be 
calculated (based on IMAGE_VIEW_FT variable) and a speed photo will be
taken and saved in an images folder. If log_data_to_file=True then a
speed_track.log file will be created/updated with event data stored in
CSV (Comma Separated Values) format.
 
Here is a YouTube demo and code walkthrough of this program https://youtu.be/eRi50BbJUro
 
Some of this code is based on a YouTube tutorial by
Kyle Hounslow using C here https://www.youtube.com/watch?v=X6rPdRZzgjg

Here is a previous YouTube video demonstrating a motion tracking test program
using a Raspberry Pi B2 https://youtu.be/09JS7twPBsQ

### Quick Setup

Requires a Raspberry Pi computer with a RPI camera module installed, configured
and tested to verify it is working. I used a RPI model B2 but a B+ or 
earlier should work OK.

Install dependencies and program per the following
login via SSH or use a desktop terminal session and perform the following

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y python-opencv python-picamera python-image python-pyexiv2
    cd ~
    mkdir speed-track
    cd speed-track
    wget https://raw.github.com/pageauc/motion-track/master/speed-track/speed_track.py
    wget https://raw.github.com/pageauc/motion-track/master/speed-track/speed_settings.py
    wget https://raw.github.com/pageauc/motion-track/master/speed-track/speed_track.md
    chmod +x speed_track.py
    python ./speed_track.py

You can also use git clone to copy the files to your RPI.

    cd ~
    git clone https://github.com/pageauc/motion-track.git
 
The speed-track files will be in the motion-track/speed-track subfolder. You can
then move them to another location if you wish.
 
Note an images folder will be created to store jpg speed photos. There is an
image_path variable in the speed-settings.py file.  Use nano editor to
change variables in this file as desired.

Use the calibrate option and follow instructions below to calculate an accurate
value for IMAGE_VIEW_FT variable in the speed_settings.py
    
### Calibrate IMG_VIEW_FT variable
  
speed_track.py needs to be calibrated in order to display a correct speed.

#### Calibration Procedure

* Setup the RPI camera to point to the view to be monitored.
* Login to RPI using SSH or desktop terminal session and cd to speed-track folder
* Use nano to edit speed_settings.py. Edit variable calibrate=True  ctl-x y to save
* Start speed_track.py eg python ./speed_track.py
* Motion will automatically be detected and calibration images will be
  put in images folder with prefix calib-
* Monitor progress and calibration images. Press ctrl-c to Quit when done. 
* Adjust the y_upper and y_lower variables to cover the road area.  Note
  image 0,0 is the top left hand corner and values are in pixels.  Do not
  exceed the CAMERA_HEIGHT default 240 value  
* Open calibration images with an image viewer program and use hash marks to
  record pixels for vehicle length
  Note each division is 10 pixels.  I use filezilla to transfer files to/from
  my PC and the RPI using sftp protocol and the RPI IP address.
* Use formula below to calculate a value for IMG_VIEW_FT variable   
  You should use several photos to confirm and average results.
* Use nano to edit the speed_settings.py and change IMG_VIEW_FT variable value
  to new calculated value.  Also change variable calibrate = False
* Restart speed_track.py and monitor console messages.
  Perform a test using a vehicle at a known speed to verify calibration.
* Make sure y_upper and y_lower variables are correctly set for the area to
  monitor. This will restrict motion detection to area between these variable
  values.  Make sure top of vehicles is included.
  
Please note that if road is too close and/or vehicles are moving too quickly then
the camera may not capture motion and/or record vehicle in speed photo.
  
#### Calibration formula
Use this formula to calculate a value for IMG_VIEW_FT
 
IMG_VIEW_FT = (CAMERA_WIDTH * Ref_Obj_ft) / num_px_for_Ref_Object

eg (320 * 18) / 80 = 72
  
###Settings

Variable values are stored in the speed_settings.py file and are imported
when speed_track.py is run.  Use the nano editor to modify these settings
per the comments.  Most settings should be OK and need not need to be
changed other will may need to be fine tuned.  The openCV settings most
likely won't need to be changed unless you are familiar with them.

Have Fun

Claude Pageau

YouTube Channel https://www.youtube.com/user/pageaucp


GitHub https://github.com/pageauc
