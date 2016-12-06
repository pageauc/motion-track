

I connected a Motion Tracking Raspberry Pi to a WIFI-LEDstripe-Controller (NodeMCU)

WHAT and WHY:
I used a Rasperry Pi to control my LED stripes per UDP. I used the motion3-track.py file as a starting point, and thought maybe someone could use this for a starting point to do some more useful things than making funny things in a hallway ;)

NEEDED EQUIPMENT:

  -NodeMCU (ESP8266 development board)
  -Raspberry Pi (I used the B+ model)
  -PowerSupply (choose whisely)
  -digital-RGB-LED stripes (i used some INK1003 controlled stripes. but I think the used arduino-libary will fit most tyoes)
  -Level-shifter to amplify the 3.3V signals from the node to 5V signals which are needed by most LED controller chips


NOTE:

  -You will have to provide enogh energy to the Raspberry.
  -The nodeMCU can be powered with 5V on the VIN pin. So if you are smart, take 5V LEDstripes ;)  

INSTALLATION:

STEP!: The Raspberry Pi part
install the needed packages on your Raspberry Pi (suggesting you use some actual version (date: 4.12.2016))
in my case it was done by only install these:

    sudo apt-get install python-opencv python-picamera
    sudo apt-get install lightdm
    sudo apt-get install lubuntu-core xvfb x11vnc
    mkdir motion-track
    cd motion-track
    wget https://github.com/lustigerluke/motion-track/tree/master/UDPcontrolledLED/motion-track.py

the motion-track.py file was my starting point. The wget version is my copy of the original motion-track.py

STEP2: The nodeMCU part
connect your nodeMCU to a PC running ArduinoIDE. get the needed additional BoardManager Adresses and set them in settns, Now go to Board-Manager and add "ESP8266" or "nodemcu". Load the needed Boards and you are ready to go. 
Connect your NodeMCU and upload the *.ino file.
You will now have to do some soldering with the Node and the PowerSupply and the LevelShifter. If you know what you are doing everything is straight forward.

NOTE: the needed board manager adress to add should be: http://arduino.esp8266.com/stable/package_esp8266com_index.json


have fun and be nice with comments because I am new to this documentation thing ;)
