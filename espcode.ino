#include <ESP8266WiFi.h>        // Include the Wi-Fi library
#include <ESP8266WebServer.h>   // For using server 

const char* ssid     = "vivo";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "12345678";        // The password of the Wi-Fi network

ESP8266WebServer server(80);

#define in1 D2
#define in2 D3
#define in3 D4
#define in4 D5
#define ena D6
#define enb D7

void setup() {
  Serial.begin(115200);         // Start the Serial communication to send messages to the computer


  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(ena, OUTPUT);
  pinMode(enb, OUTPUT);

  digitalWrite(in1, 1);
  digitalWrite(in2, 0);
  digitalWrite(in3, 0);
  digitalWrite(in4, 1);

  Serial.println('\n');
  WiFi.begin(ssid, password);             // Connect to the network
  Serial.print("Connecting to ");
  Serial.print(ssid); Serial.println(" ...");

  int i = 0;
  while (WiFi.status() != WL_CONNECTED) { 
   delay(500);
    Serial.print(++i); Serial.print(' ');
  }

  Serial.println('\n');
  Serial.println("Connection established!");
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());         // Send the IP address of the ESP8266 to the computer

  server.on("/forward", forward);
  server.on("/halt", halt);
  server.on("/left", left);
  server.on("/right", right);

  server.begin();
}

void loop() {
  server.handleClient();
}

void forward()
{
  server.send(200);

  analogWrite(ena , 912);
  analogWrite(enb , 912);
}

void halt() 
{
  server.send(200);
   
  digitalWrite(ena , LOW);
  digitalWrite(enb , LOW);

}

void left()
{
  server.send(200);
   Serial.println('L');
  analogWrite(ena, 812);
  digitalWrite(enb , LOW);
}


void right()
{
  server.send(200);
 analogWrite(enb, 812);
  digitalWrite(ena , LOW);
}
