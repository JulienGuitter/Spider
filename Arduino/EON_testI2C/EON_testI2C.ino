#include <Wire.h>

#define UNO_ADDR    9
#define RESP_SIZE   150

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin(UNO_ADDR);
  Serial.println("Setup");
  /* Event Handler */
  Wire.onReceive(DataReceive);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(50);
}


void DataReceive(int numBytes){
  int i=0;
  char data[RESP_SIZE];
  memset(data, 0, RESP_SIZE);
  while(Wire.available()){
    data[i++]=Wire.read();
  }

  Serial.print("Recv Event : ");
  Serial.println(String(data));
}