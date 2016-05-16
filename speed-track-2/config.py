# ---------------- User Configuration Settings for speed2.py ---------------------------------

# Display and Log settings
verbose = True              # display basic status information on console
calibrate = False           # Create a speed_calibrate.jpg file with markers to calculate a px to FT conversion
display_fps = True         # show average frame count every 100 loops
gui_window_on = False       # Display desktop GUI openCV threshold window. Set to False if running from ssh console only.
log_data_to_file = True     # save log data as CSV comma separated values

# Motion Event Settings
# ---------------------
IMAGE_VIEW_FT = 72     # Set the width in feet for the road width that the camera width sees
SPEED_MPH = True       # Set the speed conversion  kph = False  mph=True
MIN_AREA = 500         # Exclude all contours less than or equal to this sq-px Area
y_upper = 120          # Exclude motion above this point to top of image.
y_lower = 200          # Exclude motion below this point to bottom of image.
max_speed_over = 0     # Exclude Speed less than or equal to value specified 0=All 
track_len_trig  = 100  # Length of track to trigger speed photo
event_timeout = 2      # Number of seconds to wait between motion events before starting new track
x_diff_min = 3         # min px away from last motion event x pos
x_diff_max = 100       # max px away for last motion event x pos

# Camera Settings
CAMERA_ROTATION = 0    # Rotate camera image valid values are 0, 90, 180, 270
CAMERA_VFLIP = False   # Flip the camera image vertically if required
CAMERA_HFLIP = False   # Flip the camera image horizontally if required

# Speed Photo Camera Image Settings
image_path = "images"     # folder name to store images 
image_prefix = "cam1-"    # image name prefix
image_text_bottom = True  # True = Show image text at bottom otherwise at top
image_font_size = 20      # px height of font on images default = 20
image_bigger = 3          # multiply value to resize the default image size 320x240
 
# OpenCV Motion Tracking Settings
WINDOW_BIGGER = 3  # resize multiplier for opencv window if gui_window_on=True default = 3
CIRCLE_SIZE = 1    # diameter of circle to show motion location in window
BLUR_SIZE = 10     # OpenCV setting for Gaussian difference image blur 
THRESHOLD_SENSITIVITY = 25  # OpenCV setting for difference image threshold

#--------------------------- End of User Settings -------------------------------------------------
