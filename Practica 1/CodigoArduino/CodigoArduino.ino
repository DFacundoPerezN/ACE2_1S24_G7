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
String direccion;
String tipo;
String rol="ajeno";

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for Serial Monitor to open

  if (!APDS.begin()) {
    Serial.println("Error initializing APDS-9960 sensor.");
    while (true); // Stop forever
  }
}

int proximity = 0;
int r = 0, g = 0, b = 0;
unsigned long lastUpdate = 0;

void loop() {

  // Check if a proximity reading is available.
  if (APDS.proximityAvailable()) {
    proximity = APDS.readProximity();
  }

  // Check if a gesture reading is available
  if (APDS.gestureAvailable()) {
    int gesture = APDS.readGesture();
    switch (gesture) {
      case GESTURE_UP:
        //Serial.println("Detected UP gesture");
        direccion = "ingreso";
        break;

      case GESTURE_DOWN:
        //Serial.println("Detected DOWN gesture");
        direccion = "regreso";
        break;

      case GESTURE_LEFT:
        //Serial.println("Detected LEFT gesture");
        direccion = "ingreso";
        break;

      case GESTURE_RIGHT:
        //Serial.println("Detected RIGHT gesture");
        direccion = "regreso";
        break;

      default:
        // Ignore
        break;
    }
  }

  // Check if a color reading is available
  if (APDS.colorAvailable()) {
    APDS.readColor(r, g, b);
  }

  // Print updates every 100 ms
  if (millis() - lastUpdate > 100) {
    lastUpdate = millis();
    //Serial.print("PR=");
    //Serial.print(proximity);
    if(proximity<150){
      tipo = "grande";
    }else if(proximity<750){
      tipo = "mediano";
    }else {
      tipo = "pequeño";
    }
    Serial.print(" RGB=");
    Serial.print(r);
    Serial.print(",");
    Serial.print(g);
    Serial.print(",");    
    Serial.println(b);
    if((b-r)>50 && b>g){//azul
      rol="trabajador";
    }else if((r-g)>75){//rojo
      rol="estudiante";
    }else if(g>150 && g>b && abs(g-r)<50){
      rol="catedratico";
    }else{
      rol="ajeno";
    }
    Serial.println(tipo+";"+rol+";"+direccion);
  }
}
