# ---------------- User Configuration Settings for speed-track.py ---------------------------------

# Set display and log settings
verbose = True         # display basic status information on console
display_fps = False    # show average frame count every 100 loops
log_data_to_file = True   # save comma delimited file to a text .log file
gui_window_on = False  # Display desktop GUI openCV threshold window. Set to False if running from ssh console only.
calibrate = False      # Create a speed_calibrate.jpg file with markers to calculate a px to FT conversion

# Motion Camera Settings
CAMERA_HFLIP = False   # Flip the camera image horizontally if required
CAMERA_VFLIP = False   # Flip the camera image vertically if required
CAMERA_WIDTH = 320     # Set the image stream width for opencv motion scanning
CAMERA_HEIGHT = 240    # Set the image stream height for opencv motion scanning
WINDOW_BIGGER = 3      # if gui_window_on=True then multiplies the opencv window size by this amount
IMAGE_VIEW_FT = 72     # Set the width in feet for the road width that the camera width sees
SPEED_MPH = True       # Set the speed conversion  kph = False  mph=True

# Speed Photo Camera Image Settings
image_width = 1280      # Set width of trigger point image to save 
image_height = 720      # Set height of trigger point image to save
image_path = "images"   # folder name to store images 
image_prefix = "speed-" # image name prefix
image_text_bottom = True  # True = Show image text at bottom otherwise at top

# Motion Tracking Settings

MIN_AREA = 200     # excludes all contours less than or equal to this Area
CIRCLE_SIZE = 1    # diameter of circle to show motion location in window
BLUR_SIZE = 10     # OpenCV setting for Gaussian difference image blur 
THRESHOLD_SENSITIVITY = 25  # OpenCV setting for difference image threshold

# Motion Event Settings
# ---------------------
event_timeout = 2  # Number of seconds to wait between motion events before clearing track

# Set valid range for next motion event before appending (excludes unrealistic speeds)
x_diff_min = 2
x_diff_max = 130

# Set cumulative track length trigger point for taking speed photo
# Note: Fast motion may not get captured due to camera lag.
track_trig_len  = 160

# Set valid y Limits for motion events.  This restricts valid motion to road area.
y_upper = 140   # Exclude motion events above this point to top of image.
y_lower = 200   # Exclude motion events below this point to bottom of image.


#--------------------------- End of User Settings -------------------------------------------------
