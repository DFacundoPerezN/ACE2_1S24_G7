#include <Servo.h>
#include <Mouse.h>

Servo myServo;  
const int trigpin1= 8;  
const int echopin1= 7;  
long duration;  
int distance;  
int distancias[5] ={0,0,0,0,0};

void setup() {
  pinMode(trigpin1,OUTPUT);  
  pinMode(echopin1,INPUT); 
  myServo.attach(4);
  myServo.write(0);
  Serial.begin(9600);
}

void loop() {
  int contadorLista = 0;
  pruebaDistancias(18);
  // for(int angle = 90; angle >= -90; angle -= 18) {
  //   myServo.write(angle);
  //   digitalWrite(trigpin1, HIGH);  
  //   delayMicroseconds(25);  
  //   digitalWrite(trigpin1, LOW);  
  //   duration = pulseIn(echopin1, HIGH);  
  //   distance = duration * 0.034 / 2;  
  //   Serial.println(distance);  
  //   Serial.print("--"); 
  //   Serial.println(contadorLista); 
  //   delay(400);  
  //   decidirGuardar(distance, contadorLista);
  //   contadorLista++;
  //   delay(400);
  // }

  //impirmirDistancias();
  
  Serial.println("\n \n \n "); 
}

void impirmirDistancias(){
  Serial.println(sizeof(distancias));  
  Serial.println("\n \n ");  
  delay(40);
  for (int i=0; i < sizeof(distancias)-1;i++){
    Serial.println(distancias[i]); 
  }
}

void decidirGuardar(int distance, int contador){
  if (contador != 2 && contador < 6){
    if(contador < 2){
      distancias[contador]=distance;
      Serial.println("Seguardo la distancia ");
    }
    else{      
      distancias[contador-1]=distance;
      Serial.println("Seguardo la distancia ");
    }
  }
}

void pruebaDistancias(int angle){
  myServo.write(angle);
  digitalWrite(trigpin1, HIGH);  
  delayMicroseconds(25);  
  digitalWrite(trigpin1, LOW);  
  duration = pulseIn(echopin1, HIGH);  
  distance = duration * 0.034 / 2;  
  Serial.println(distance);  
  delay(700);

}
