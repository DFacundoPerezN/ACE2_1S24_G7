#include <cvzone.h>

SerialData serialData(4,1);
int valsRec[4];

void setup() {
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(7, OUTPUT); 
  serialData.begin(9600);
}

void loop() {
    serialData.Get(valsRec);
    digitalWrite(13, valsRec[0]);
    digitalWrite(12, valsRec[1]);
    digitalWrite(8, valsRec[2]);
    digitalWrite(7, valsRec[3]);
    delay(10);
}
