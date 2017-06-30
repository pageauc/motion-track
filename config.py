# Config.py file for motion-track.py  Release 1.00

# Display Settings
# ----------------
debug = True        # Set to False for no data display
window_on = False   # Set to True displays opencv windows (GUI desktop reqd)
show_fps = False    # Show Frames per second 

# OpenCV Settings
# ---------------
diff_window_on = False # Show OpenCV image difference window
thresh_window_on = False  # Show OpenCV image Threshold window
SHOW_CIRCLE = True  # True= show circle False= show rectancle on biggest motion
CIRCLE_SIZE = 8     # diameter of circle for SHOW_CIRCLE
LINE_THICKNESS = 1  # thickness of bounding line in pixels
WINDOW_BIGGER = 1   # Resize multiplier for Movement Status Window
                    # if gui_window_on=True then makes opencv window bigger
                    # Note if the window is larger than 1 then a reduced frame rate will occur            

# Camera Settings
# ---------------
WEBCAM = False        # False= Pi Camera  True= USB Web Camera( Must be plugged into a USB socket)
CAMERA_WIDTH = 320    # default = 320  can be greater if quad core RPI
CAMERA_HEIGHT = 240   # default = 240    
CAMERA_HFLIP = False  # True=flip camera image horizontally
CAMERA_VFLIP = False  # True=flip camera image vertically
CAMERA_ROTATION = 0   # Rotate camera image valid values 0, 90, 180, 270
CAMERA_FRAMERATE = 25 # default = 25 lower for USB Web Cam. Try different settings
FRAME_COUNTER = 1000  # used when show_fps=True  Sets frequency of display

# Motion Track Settings
# ---------------------
MIN_AREA = 200       # excludes all contours less than or equal to this Area
THRESHOLD_SENSITIVITY = 25
BLUR_SIZE = 10
