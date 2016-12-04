

I connected a Motion Tracking Raspberry Pi to a WIFI-LED-Controller (NodeMCU)

WHAT and WHY:
I used a Rasperry Pi to control my LED stripes per UDP. I used the motion3-track.py file as a starting point, and thought maybe someone could use this for a starting point to do some more useful things than making funny things in a hallway ;)

NEEDED EQUIPMENT:

  -NodeMCU (ESP8266 development board)
  -Raspberry Pi (I used the B+ model)
  -PowerSupply (choose whisely)
  -digital-RGB-LED stripes (i used some INK1003 controlled stripes. but I think the used arduino-libary will fit most tyoes)
  -Level-shifter to amplify the 3.3V signals from the node to 5V signals which are needed by most LED controller chips


NOTE:

  -You will have to provide enogh energy to the Raspberry. \l
  -The nodeMCU can be powered with 5V on the VIN pin. So if you are smart, take 5V LEDstripes ;)  
