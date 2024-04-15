#include <Servo.h>
#include <Mouse.h>

Servo myServo;  
const int trigpin= 8;  
const int echopin= 7;  
long duration;  
int distance;  

void setup() {
  pinMode(trigpin,OUTPUT);  
  pinMode(echopin,INPUT); 
  myServo.attach(4);
  myServo.write(0);
  Serial.begin(9600);
}

void loop() {
  for(int angle = 90; angle >= -90; angle -= 18) {
    myServo.write(angle);
    digitalWrite(trigpin, HIGH);  
    delayMicroseconds(25);  
    digitalWrite(trigpin, LOW);  
    duration = pulseIn(echopin, HIGH);  
    distance = duration * 0.034 / 2;  
    Serial.println(distance);  
    delay(400);
  }
  Serial.println("\n \n \n ");  
  delay(800);

}
