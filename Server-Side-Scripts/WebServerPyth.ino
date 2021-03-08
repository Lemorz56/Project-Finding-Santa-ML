#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include "password.h"

ESP8266WebServer server;

void setup() 
{
  pinMode(2, OUTPUT);
  pinMode(15, OUTPUT);
  //pinMode(14, OUTPUT);
  
  Serial.begin(115200);
  Serial.print("Setting pin 2 to LOW \n");
  digitalWrite(2, LOW);
  
  Serial.print("Connecting");
  WiFi.begin(ssid, password);
  while(WiFi.status()!=WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("IP Address: ");
  Serial.print(WiFi.localIP());
  
  server.on("/",[](){server.send(200, "text/plain", "Hello Test");});
  server.on("/toggleON",toggleON);
  server.on("/toggleOFF",toggleOFF);
  server.begin();
  toggleOFF();
}

void loop() 
{
  server.handleClient();
}

void toggleON()
{
  digitalWrite(2, LOW);
  digitalWrite(15, HIGH);
  server.send(200, "Light Touched");
}

void toggleOFF()
{
  digitalWrite(2, HIGH);
  digitalWrite(15, LOW);
  server.send(200, "Light OFF");
}