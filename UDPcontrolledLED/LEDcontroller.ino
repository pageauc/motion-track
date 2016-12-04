
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "FastLED.h"
#include <QueueList.h>

//WIFI CONFIG
char ssid[] = "Floppy_Disk_W2"; //  your network SSID (name)
char pass[] = "Luc1lle#";       // your network password
//char ssid[] = "/dev/lol"; //  your network SSID (name)
//char pass[] = "4dprinter";       // your network password
unsigned int localPort = 2390;  // local port to listen for UDP packets

//LED CONFIG
#define NUM_LEDS 60             // How many leds in your strip?
#define DATA_PIN 1              // Status LED
#define DATA_PIN1 3             // Leiste 1
#define DATA_PIN2 4             // Leiste 2

CRGB statusled[1];
CRGB leds[NUM_LEDS];
QueueList <int> queue;
int TRACE_COUNT = 7;
int TRACE_TIME = 2000;
unsigned long previousMillis = 0;        // will store last time LED was updated
unsigned long currentMillis = millis();


// A UDP instance to let us send and receive packets over UDP
const int NTP_PACKET_SIZE = 48; // NTP time stamp is in the first 48 bytes of the message
byte packetBuffer[ NTP_PACKET_SIZE]; //buffer to hold incoming and outgoing packets
WiFiUDP udp;

void setup()
{
  Serial.begin(115200);
  Serial.println();
  Serial.println();

  // We start by connecting to a WiFi network
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Starting UDP");
  udp.begin(localPort);
  Serial.print("Local port: ");
  Serial.println(udp.localPort());


  Serial.print("LED setup: ");
  FastLED.addLeds<WS2812B, DATA_PIN>(statusled, 1);
  FastLED.addLeds<WS2812B, DATA_PIN1>(leds, NUM_LEDS);
  FastLED.addLeds<WS2812B, DATA_PIN2>(leds, NUM_LEDS);  

  for(int x = 0; x < NUM_LEDS ; x++){  leds[x] = CRGB::Blue;}
  FastLED.show();   //update led stripe
  
  Serial.println("done!");
}

void loop()
{

  //  int adr;
  int red;
  int gre;
  int blu;
  int cb = udp.parsePacket();
  char charMatrix[cb];
  String package;


  
  if (!cb) {
    //do nothing 
    //repeat waiting for udp message
  }
  else {
    Serial.print("packet received, length=");
    Serial.println(cb);  //print length
    // We've received a packet, read the data from it
    udp.read(packetBuffer, NTP_PACKET_SIZE); // read the packet into the buffer

 //read and process data

    //convert every byte to a character
    int i=0;  
    while(i<cb){
      charMatrix[i]= char (packetBuffer[i]);
      i++;
    }

    //convert the character array to String
    package=charMatrix;
    Serial.println(package);


    //read first int value (adress)
    Serial.print("adress:");
    int adr = package.toInt();
    Serial.println(adr);
    package=package.substring(6); //delete the first int value and the seperator char

    //read second int value (RED)
    Serial.print("red value:");
    red = package.toInt();
    Serial.println(red);
    package=package.substring(6);

    //read third int value (GREEN)
    Serial.print("green value:");
    gre = package.toInt();
    Serial.println(gre);
    package=package.substring(6);
    
    //read fourth int value (BLUE)
    Serial.print("blue value:");
    blu = package.toInt();
    Serial.println(blu);

    leds[adr] = CRGB(red,gre,blu);
     
    
    //turn off old LEDs
    if(queue.count()>TRACE_COUNT)
    {
      leds[queue.pop()] = CRGB(0,0,0);
      
    }//endif
    queue.push(adr);

    previousMillis = millis();

    FastLED.show();   //update led stripe
    
  } //else (end what t0 do if input was available)

  //delay without delay ;)
  currentMillis = millis();
  if (currentMillis - previousMillis >= TRACE_TIME && !queue.isEmpty()) {
    previousMillis = currentMillis;
    leds[queue.pop()] = CRGB(0,0,0);
    FastLED.show();   //update led stripe    
  } //endif

}//loop

