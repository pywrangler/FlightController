#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include<Servo.h>

#define D0 16 //dev board LED
#define D1 5
#define D2 4
#define D3 0
#define D4 2  //this lights up the esp main module LED
#define D5 14
#define D6 12
#define D7 13
#define D8 15
#define D9 3
#define D10 1


Servo ser1, ser2,bldc;
const char* ssid = "controlServ";
const char* password = "darksector";

WiFiUDP Udp;
unsigned int localUdpPort = 4210;  // local port to listen on
char inc[255];
char IPbuff[400];
IPAddress cliIP;
int cliPort;
int packetSize;

void autoflight(){
  ser1.write(85);
  ser2.write(85);
  bldc.write(0);
}
void connectwifi(){
  Serial.begin(115200);
  Serial.println();
  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");

  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
  Serial.end();
}
void setup()
{
  ser1.attach(D5);
  ser2.attach(D6);
  bldc.attach(D7);
  bldc.write(0);
  ser1.write(85);
  ser2.write(85);
  pinMode(D8, INPUT);//takes low battery interrupt
  pinMode(D4, OUTPUT);//keeps the LED lit af
  connectwifi();
 // Serial.println("waiting for controller host IP");
//  while(1){
//    int ackpack = Udp.parsePacket();
//  if (ackpack<=42 && ackpack>1)
//  {
//    // receive incoming UDP packets
//    //Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
//    cliIP = Udp.remoteIP();
//    char cliPortstr[255];
//    Udp.read(cliPortstr,255);
//    cliPort = atoi(cliPortstr);
//    
//    Serial.println(cliIP.toString().c_str());
//    Serial.println(cliPort);
//    Udp.beginPacket(cliIP, cliPort);
//    Udp.write("host and ip received ");
//    Udp.write(cliIP.toString().c_str());
//    Udp.write("PORT: ");
//    Udp.write(cliPortstr);
//    Udp.endPacket();
//    break;
//    }
  //}
  //Serial.end();
  //END SERIAL COMMUNICATION
}

int _s1, _s2, _fsp;

void fatoi(const char *str) {
  int i = 0, s1 = 0, s2 = 0, fsp = 0;
  while (i < 3) {
    s1 *= 10;
    s1 += *str - '0';
    *str++;
    i++;
  }
  _s1 = s1;
  while (i < 6) {
    s2 *= 10;
    s2 += *str - '0';
    *str++;
    i++;
  }
  _s2 = s2;
  while (i < 9) {
    fsp *= 10;
    fsp += *str - '0';
    *str++;
    i++;
  }
  _fsp = fsp;
}
void loop()
{
  
  packetSize = Udp.parsePacket();
  //Serial.println("udp.parse ended");
  if (packetSize)
  {
    // receive incoming UDP packets
    //Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    Udp.read(inc, 255);
    //    if (len > 0)
    //    {
    //      incomingPacket[len] = 0;
    //    }
    //Serial.printf("UDP packet contents: %s\n", incomingPacket);
    fatoi(inc);
    
    ser1.write(_s1);
    ser2.write(_s2);
    bldc.write(_fsp);
    //Serial.printf(" ipack is %d ",intpack);
    //Serial.printf("s1: %d s2: %d fsp: %d ", _s1,_s2,_fsp);
    //Serial.println();
    //servo.write( atoi(incomingPacket) );
    // send back a reply, to the IP address and port we got the packet from
    //Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    //Udp.write(replyPacekt);
    //Udp.endPacket();
    }
    else if (WiFi.status() == WL_CONNECTION_LOST || WiFi.status() == WL_DISCONNECTED )
  {
  autoflight();
  connectwifi();
  }
    //Serial.println("if packsize ended");
//  if (digitalRead(D8)) {           //digitalRead(D8)==HIGH
//      Udp.beginPacket(cliIP, cliPort);
//      Udp.write("***LOW BATTERY***");
//      Udp.endPacket();
//    }
}
