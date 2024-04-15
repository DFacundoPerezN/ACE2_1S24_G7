/*
  APDS-9960 - All sensor data from APDS-9960

  This example reads all data from the on-board APDS-9960 sensor of the
  Nano 33 BLE Sense:
   - color RGB (red, green, blue)
   - proximity
   - gesture
  and prints updates to the Serial Monitor every 100 ms.

  The circuit:
  - Arduino Nano 33 BLE Sense

  This example code is in the public domain.
*/

#include <Arduino_APDS9960.h>
#include <Arduino.h>

#define sens/*
  APDS-9960 - All sensor data from APDS-9960

  This example reads all data from the on-board APDS-9960 sensor of the
  Nano 33 BLE Sense:
   - color RGB (red, green, blue)
   - proximity
   - gesture
  and prints updates to the Serial Monitor every 100 ms.

  The circuit:
  - Arduino Nano 33 BLE Sense

  This example code is in the public domain.
*/

#include <Arduino_APDS9960.h>
#include <Arduino.h>

#define echoPin 11
#define trigPin 12 
#define sensorPinEntry 9
#define sensorPinExit 7

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for Serial Monitor to open

  if (!APDS.begin()) {
    Serial.println("Error initializing APDS-9960 sensor.");
    while (true); // Stop forever
  }

  pinMode(trigPin,OUTPUT);
  pinMode(echoPin,INPUT);
  pinMode(sensorPinEntry, INPUT);
  pinMode(sensorPinExit, INPUT);
}

int proximity = 0;
int r = 0, g = 0, b = 0;
int gesture = -1;
unsigned long lastUpdate = 0;


void loop() {
  String direction;
  long duration,distance;
  int goingIn, GoingOut;

  goingIn = digitalRead(sensorPinEntry);
  GoingOut = digitalRead(sensorPinExit);

  if (goingIn == HIGH && GoingOut == LOW) {//entrando
    while(digitalRead(sensorPinExit)==LOW){//mientras no pase por salida

      if (APDS.proximityAvailable()) {
      proximity = APDS.readProximity();
      }

      // Check if a gesture reading is available
      if (APDS.gestureAvailable()) {
        gesture = APDS.readGesture();
      }
      direction = "entrando";

      // Check if a color reading is available
      if (APDS.colorAvailable()) {
        APDS.readColor(r, g, b);
      }

      distance = ultraSonicShot();
    }

  }else if (goingIn == LOW && GoingOut == HIGH){
    
    while(digitalRead(sensorPinEntry)==LOW){
    if (APDS.proximityAvailable()) {
    proximity = APDS.readProximity();
    }

    // Check if a gesture reading is available
    if (APDS.gestureAvailable()) {
      gesture = APDS.readGesture();
    }
    direction = "saliendo";

    // Check if a color reading is available
    if (APDS.colorAvailable()) {
      APDS.readColor(r, g, b);
    }

    distance = ultraSonicShot();
    }

  } 


 //HACER REVISION DE LA OBTENCION DE MOVIMIENTO; PARA QUE SE DETECTEN AL MISMO TIEMPO QUE DISTANCIA Y RGB
  // Print updates every 100 ms
  if (millis() - lastUpdate > 500) {
    lastUpdate = millis();
    Serial.print("DR="+direction);
    Serial.print(" PR=");
    Serial.print(distance);
    Serial.print(" RGB=");
    Serial.print(r);
    Serial.print(",");
    Serial.print(g);
    Serial.print(",");
    Serial.println(b);
  }
  gesture = -1;
}


long ultraSonicShot(){
    long duration, distance;
  
    // Check if a proximity reading is available.
    digitalWrite(trigPin,LOW);
    delay(2);
    digitalWrite(trigPin,HIGH);
    delay(10);
    digitalWrite(trigPin,LOW);
    duration = pulseIn(echoPin,HIGH);
    distance = (duration/2) / 29.1;
    return distance;
}



