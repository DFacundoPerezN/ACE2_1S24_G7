const int buttonPin = 5; // Pin del botón
int buttonState = 0;     // Variable para almacenar el estado del botón
#include <Servo.h>

Servo servoX;
Servo servoY;
Servo servoWidth;
Servo servoHeight;


void setup() {
  Serial.begin(9600);    // Inicializar comunicación serial
  pinMode(buttonPin, INPUT); // Configurar pin del botón como entrada
  servoX.attach(9);
  servoY.attach(10);
}

void loop() {
  buttonState = digitalRead(buttonPin); // Leer estado del botó
  if (buttonState == HIGH) {
    delay(7000);  // Si el botón está presionad++++
    Serial.println('1'); // Enviar mensaje por serial // Esperar 1 segundo para evitar rebotes
    delay(5000);
  } 
  else{
    Serial.println('0');
  }
  if (Serial.available() > 0) {
    // Leer la cadena de entrada desde Python
    String entrada = Serial.readStringUntil('\n');
    
    // Analizar la cadena para obtener los valores de los servomotores
    int valores[2];
    int index = 0;
    char *ptr = strtok(const_cast<char*>(entrada.c_str()), ",");
    while (ptr != NULL && index < 4) {
      valores[index++] = atoi(ptr);
      ptr = strtok(NULL, ",");
    }
    
    // Mover los servomotores a las posiciones especificadas
    servoX.write(valores[0]);
    servoY.write(valores[1]);
  }
}   