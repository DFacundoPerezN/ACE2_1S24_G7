
#include <Servo.h>
#include <Mouse.h>

Servo myServo1;  
Servo myServo2;  
Servo myServo3;  
Servo myServo4;  
Servo myServo5;  
const int trigpin1= 7;  
const int echopin1= 6;  

const int trigpin2= 13;  
const int echopin2= 12;  

const int trigpin3= 28;  
const int echopin3= 26; 

const int trigpin4= 35;  
const int echopin4= 33; 

const int trigpin5= 53;  
const int echopin5= 52;  

long duration;  
int distance;  
//int distancias[5] ={0,0,0,0,0};
String salida = "Habitacion1:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0";
String salida2 = "Habitacion2:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0";
String salida3 = "Habitacion3:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0";
String salida4 = "Habitacion4:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0";
String salida5 = "Habitacion5:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0";

void setup() {
  pinMode(trigpin1,OUTPUT);  
  pinMode(echopin1,INPUT); 
  pinMode(trigpin2,OUTPUT);  
  pinMode(echopin2,INPUT); 
  pinMode(trigpin3,OUTPUT);  
  pinMode(echopin3,INPUT); 
  pinMode(trigpin4,OUTPUT);  
  pinMode(echopin4,INPUT); 
  pinMode(trigpin5,OUTPUT);  
  pinMode(echopin5,INPUT); 
  myServo1.attach(4);
  myServo2.attach(10);
  myServo3.attach(50);
  myServo4.attach(31);
  myServo5.attach(45);
  myServo1.write(0);
  Serial.begin(9600);
}

void map1Position(int angulo,int distancia) {
  switch (angulo) {
  case 90:
    if (distancia >= 7 && distancia <= 8) {
      salida[12] = '1';
    //  Serial.println("Se leyo persona en 0,0");  
    } else if (distancia >= 4 && distancia <= 5) {
      salida[14] = '1';
    //  Serial.println("Se leyo persona");  
      //return salida;
    } else if (distancia >=2 && distancia <= 3) {
      salida[16] = '1';
    //  Serial.println("Se leyo persona");  
    }
    break;
  case 75:
    if (distancia >= 6 && distancia <= 8) {
      salida[20] = '1';
    //  Serial.println("Se leyo persona en 0,1");  
    } else if (distancia >= 4 && distancia <= 5){
      salida[22] = '1';
     // Serial.println("Se leyo persona");  
    } else if (distancia <= 2){
      salida[24] = '1';
    //  Serial.println("Se leyo persona");  
    }
    break;
  case 60:
    if (distancia >= 10 && distancia <= 11) {
      salida[28] = '1';
     // Serial.println("Se leyo persona en 0,2");  
    }
    break;
  case 45:
    if (distancia >= 11 && distancia <= 11) {
      salida[36] = '1';
    //  Serial.println("Se leyo persona en 0,3");  
    } else if (distancia >= 5 && distancia <= 10){
      salida[30] = '1';
    //  Serial.println("Se leyo persona");  
    } else if (distancia <= 4){
      salida[24] = '1';
    //  Serial.println("Se leyo persona");  
    }
    break;
  case 30:
    if (distancia >= 9 && distancia <= 11) {
      salida[38] = '1';
    //  Serial.println("Se leyo persona");  
    } else if (distancia >= 3 && distancia <= 6){
      salida[32] = '1';
     // Serial.println("Se leyo persona");  
    } 
    break;
  case 15:
    if (distancia >= 7 && distancia <= 9) {
      salida[40] = '1';
     // Serial.println("Se leyo persona en 2,3");  
    }
    break;
  case 0:
    if (distancia >= 7 && distancia <= 9) {
      salida[42] = '1';
    //  Serial.println("Se leyo persona en 3,3");  
    } else if (distancia >= 3 && distancia <= 6){
      salida[34] = '1';
     // Serial.println("Se leyo persona en 3,2");  
    } else if (distancia <= 2){
      salida[26] = '1';
     // Serial.println("Se leyo persona en 3,1");  
    }
    break;
  }
}

void loop() {
  int contadorLista = 0;

  // String salidaH1 = "Habitacion1:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0"; //primer 0 en posicion [12]
  // String salidaH2 = "Habitacion2:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0"; //primer 0 en posicion [12]
  // String salidaH3 = "Habitacion3:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0"; //primer 0 en posicion [12]
  // String salidaH4 = "Habitacion4:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0"; //primer 0 en posicion [12]

  //pruebaDistancias(90);
  pruebaDistancias3(0);
  // for(int angle = 90; angle >= 0; angle -= 15) {
  //   myServo1.write(angle);
  //   myServo2.write(angle);
  //   myServo3.write(angle);
  //   myServo4.write(angle);
  //   myServo5.write(angle);
  //   digitalWrite(trigpin1, HIGH);  
  //   delayMicroseconds(25);  
  //   digitalWrite(trigpin1, LOW);  
  //   duration = pulseIn(echopin1, HIGH);  
  //   distance = duration * 0.034 / 2;  
  //   //Serial.println("");  
  //   //Serial.print(distance);  
  //   delay(700); 
  //   //Serial.print("-- en: "); 
  //   //Serial.println(angle); 
  //   map1Position(angle,distance); 
  //   //Serial.println("salidaH1 " + salida);
  //   delay(400);  
  //   //decidirGuardar(distance, contadorLista);
  //   distance = distanceH2();    
  //   Serial.print(distance);    Serial.print("-- en H2: ");     Serial.println(angle); 
  //   map2Position(angle,distance);
  //   ////contadorLista++;
  //   delay(40);  
  //   //decidirGuardar(distance, contadorLista);
  //   distance = distanceH3();    
  //   //Serial.print(distance);    Serial.print("-- en H3: ");     Serial.println(angle); 
  //   map3Position(angle,distance);
  //   delay(40);

  //   distance = distanceH4();    
  //   //Serial.print(distance);    Serial.print("-- en H4: ");     Serial.println(angle); 
  //   map4Position(angle,distance);
  //   delay(40);

  //   distance = distanceH5();    
  //   //Serial.print(distance);    Serial.print("-- en H5: ");     Serial.println(angle); 
  //   map5Position(angle,distance);
  //   delay(40);
  //   distance=0;
  //   duration =0;
  // }
  // Serial.println(salida); 
  // Serial.println(salida2);  
  // Serial.println(salida3);  
  // Serial.println(salida4);  
  // Serial.println(salida5);
  //impirmirDistancias();
  delay(400);
  //Serial.println("\n \n \n "); 
  salida = "Habitacion1:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0";
  salida2 = "Habitacion2:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0";
  salida3 = "Habitacion3:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0";
  salida4 = "Habitacion4:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0";
  salida5 = "Habitacion5:0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0";
  
}

// void impirmirDistancias(){
//   Serial.println(sizeof(distancias));  
//   Serial.println("\n \n ");  
//   delay(40);
//   for (int i=0; i < sizeof(distancias)-1;i++){
//     Serial.println(distancias[i]); 
//   }
// }

int distanceH2() {
  digitalWrite(trigpin2, HIGH);  
  delayMicroseconds(25);  
  digitalWrite(trigpin2, LOW);  
  int distance = pulseIn(echopin2, HIGH) * 0.034 / 2;
  //Serial.println(distance);  
  return  distance;
}

int distanceH3() {
  digitalWrite(trigpin3, HIGH);  
  delayMicroseconds(25);  
  digitalWrite(trigpin3, LOW);  
  return pulseIn(echopin3, HIGH) * 0.034 / 2; 
}

int distanceH4() {
  digitalWrite(trigpin4, HIGH);  
  delayMicroseconds(25);  
  digitalWrite(trigpin4, LOW);  
  return pulseIn(echopin4, HIGH) * 0.034 / 2; 
}

int distanceH5() {
  digitalWrite(trigpin5, HIGH);  
  delayMicroseconds(25);  
  digitalWrite(trigpin5, LOW);  
  return pulseIn(echopin5, HIGH) * 0.034 / 2; 
}

void pruebaDistancias(int angle){
  myServo1.write(angle);
  digitalWrite(trigpin1, HIGH);  
  delayMicroseconds(25);  
  digitalWrite(trigpin1, LOW);  
  duration = pulseIn(echopin1, HIGH);  
  distance = duration * 0.034 / 2;  
  Serial.println(distance);  
  delay(700);
}
void pruebaDistancias2(int angle){
  myServo2.write(angle);
  // digitalWrite(trigpin2, HIGH);  
  // delayMicroseconds(25);  
  // digitalWrite(trigpin2, LOW);  
  // duration = pulseIn(echopin2, HIGH);  
  // distance = duration * 0.034 / 2;  
  Serial.println(distanceH2());  
  delay(700);
}

void pruebaDistancias3(int angle){
  myServo3.write(angle);
  // digitalWrite(trigpin2, HIGH);  
  // delayMicroseconds(25);  
  // digitalWrite(trigpin2, LOW);  
  // duration = pulseIn(echopin2, HIGH);  
  // distance = duration * 0.034 / 2;  
  Serial.println(distanceH3());  
  delay(700);
}

void map2Position(int angulo,int distancia) {
  switch (angulo) {
  case 90:
    if (distancia >= 7 && distancia <= 8) {
      salida2[12] = '1'; 
    } else if (distancia >= 4 && distancia <= 5) {
      salida2[14] = '1';
    } else if (distancia >=2 && distancia <= 3) {
      salida2[16] = '1';
    }
    break;
  case 75:
    if (distancia >= 6 && distancia <= 9) {
      salida2[20] = '1';
    } else if (distancia >= 4 && distancia <= 5){
      salida2[22] = '1';
    } else if (distancia <= 2){
      salida2[24] = '1';
    }
    break;
  case 60:
    if (distancia >= 8 && distancia <= 10) {
      salida2[28] = '1';
    }
    break;
  case 45:
    if (distancia >= 11 && distancia <= 13) {
      salida2[36] = '1';
    } else if (distancia >= 6 && distancia <= 9){
      salida2[30] = '1';
    } else if (distancia <= 4){
      salida2[24] = '1';
    }
    break;
  case 30:
    if (distancia >= 9 && distancia <= 11) {
      salida2[38] = '1';
     Serial.println("Se leyo persona");  
    } else if (distancia >= 4 && distancia <= 8){
      salida2[32] = '1';
    } 
    break;
  case 15:
    if (distancia >= 7 && distancia <= 9) {
      salida2[40] = '1'; 
    }
    break;
  case 0:
    if (distancia >= 7 && distancia <= 9) {
      salida2[42] = '1';  
    } else if (distancia >= 3 && distancia <= 6){
      salida2[34] = '1'; 
    } else if (distancia >= 1 && distancia <= 2){
      salida2[26] = '1'; 
    }
    break;
  }
}

void map3Position(int angulo,int distancia) {
  switch (angulo) {
  case 90:
    if (distancia >= 6 && distancia <= 8) {
      salida3[12] = '1'; 
    } else if (distancia >= 4 && distancia <= 5) {
      salida3[14] = '1';
    } else if (distancia >=1 && distancia <= 1) {
      salida3[16] = '1';
    }
    break;
  case 75:
    if (distancia >= 7 && distancia <= 8) {
      salida3[20] = '1';
    } else if (distancia >= 4 && distancia <= 5){
      salida3[22] = '1';
    } else if (distancia >=1 && distancia <= 2){
      salida3[24] = '1';
    }
    break;
  case 60:
    if (distancia >= 10 && distancia <= 11) {
      salida3[28] = '1';
    }
    break;
  case 45:
    if (distancia >= 10 && distancia <= 13) {
      salida3[36] = '1';
    } else if (distancia >= 5 && distancia <= 9){
      salida3[30] = '1';
    } else if (distancia >= 2 && distancia <= 3){
      salida3[24] = '1';
    }
    break;
  case 30:
    if (distancia >= 7 && distancia <= 9) {
      salida3[38] = '1';
    //  Serial.println("Se leyo persona");  
    } else if (distancia >= 3 && distancia <= 6){
      salida3[32] = '1';
    } 
    break;
  case 15:
    if (distancia >= 7 && distancia <= 9) {
      salida3[40] = '1'; 
    }
    break;
  case 0:
    if (distancia >= 7 && distancia <= 8) {
      salida3[42] = '1';  
    } else if (distancia >= 3 && distancia <= 5){
      salida3[34] = '1'; 
    } else if (distancia >=1 && distancia <= 2){
      salida3[26] = '1'; 
    }
    break;
  }
}

void map4Position(int angulo,int distancia) {
  switch (angulo) {
  case 90:
    if (distancia >= 7 && distancia <= 8) {
      salida4[12] = '1'; 
    } else if (distancia >= 4 && distancia <= 5) {
      salida4[14] = '1';
    } else if (distancia >=2 && distancia <= 3) {
      salida4[16] = '1';
    }
    break;
  case 75:
    if (distancia >= 6 && distancia <= 8) {
      salida4[20] = '1';
    } else if (distancia >= 4 && distancia <= 5){
      salida4[22] = '1';
    } else if (distancia <= 2){
      salida4[24] = '1';
    }
    break;
  case 60:
    if (distancia >= 10 && distancia <= 11) {
      salida4[28] = '1';
    }
    break;
  case 45:
    if (distancia >= 11 && distancia <= 11) {
      salida4[36] = '1';
    } else if (distancia >= 5 && distancia <= 10){
      salida4[30] = '1';
    } else if (distancia <= 4){
      salida4[24] = '1';
    }
    break;
  case 30:
    if (distancia >= 9 && distancia <= 11) {
      salida4[38] = '1';
    //  Serial.println("Se leyo persona");  
    } else if (distancia >= 3 && distancia <= 6){
      salida4[32] = '1';
    } 
    break;
  case 15:
    if (distancia >= 7 && distancia <= 9) {
      salida4[40] = '1'; 
    }
    break;
  case 0:
    if (distancia >= 7 && distancia <= 9) {
      salida4[42] = '1';  
    } else if (distancia >= 3 && distancia <= 6){
      salida4[34] = '1'; 
    } else if (distancia <= 2){
      salida4[26] = '1'; 
    }
    break;
  }
}

void map5Position(int angulo,int distancia) {
  switch (angulo) {
  case 90:
    if (distancia >= 7 && distancia <= 8) {
      salida5[12] = '1'; 
    } else if (distancia >= 4 && distancia <= 5) {
      salida5[14] = '1';
    } else if (distancia >=2 && distancia <= 3) {
      salida5[16] = '1';
    }
    break;
  case 75:
    if (distancia >= 6 && distancia <= 8) {
      salida5[20] = '1';
    } else if (distancia >= 4 && distancia <= 5){
      salida5[22] = '1';
    } else if (distancia <= 2){
      salida5[24] = '1';
    }
    break;
  case 60:
    if (distancia >= 10 && distancia <= 11) {
      salida5[28] = '1';
    }
    break;
  case 45:
    if (distancia >= 11 && distancia <= 11) {
      salida5[36] = '1';
    } else if (distancia >= 5 && distancia <= 10){
      salida5[30] = '1';
    } else if (distancia <= 4){
      salida5[24] = '1';
    }
    break;
  case 30:
    if (distancia >= 9 && distancia <= 11) {
      salida5[38] = '1';
    //  Serial.println("Se leyo persona");  
    } else if (distancia >= 3 && distancia <= 6){
      salida5[32] = '1';
    } 
    break;
  case 15:
    if (distancia >= 7 && distancia <= 9) {
      salida5[40] = '1'; 
    }
    break;
  case 0:
    if (distancia >= 7 && distancia <= 9) {
      salida5[42] = '1';  
    } else if (distancia >= 3 && distancia <= 6){
      salida5[34] = '1'; 
    } else if (distancia <= 2){
      salida5[26] = '1'; 
    }
    break;
  }
}