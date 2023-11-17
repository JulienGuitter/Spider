#include <Servo.h>
#include <Wire.h>

#define A_ID          1 // 0: gauche ; 1: droite

#define NB_ART        3
#define NB_LEGS       3
#define NB_SPLIT      5

#define UNO_ADDR    8+A_ID
#define RESP_SIZE   20


Servo leg[NB_LEGS][NB_ART];
const byte legsPin[NB_LEGS][NB_ART] = {{8, 9, 10}, {5,6,7}, {2,3,4}};
int startPos[NB_ART] = {0, 90, -10};
String splitedString[NB_SPLIT];
int side;
bool newLegPos = false;


void setup() {
  Serial.begin(9600);
  Wire.begin(UNO_ADDR);
  /* Event Handler */
  Wire.onReceive(DataReceive);

  //splitString("1:90:70:80", ':');
  side = A_ID%2 ? 1 : -1;

  for(int j=0; j<NB_LEGS; j++){
    for (int i = 0; i < NB_ART; i++) {
      leg[j][i].attach(legsPin[j][i]);
    }
    setLegPos(j, startPos);
    /*
    for (int i = 0; i < NB_ART; i++) {
      leg[j][i].attach(legsPin[j][i]);
      int side = j%2 ? 1 : -1;
      int angle = i<=1 ? 90-(startPos[i]*side) : 90+(startPos[i]*side);
      leg[j][i].write(angle);
    }
    */
  }
}

Servo leg

void loop() {
  //String content = "";
  //char character;
  /*
  while(Serial.available()) {
    character = Serial.read();
        if(character == 'm'){
          newLegPos = true;
        }else if(character == 'e'){
          break;
        }else{
          content.concat(character);
          delay(10);
        }
  }
  
  if (content != "") {
    */
  if(newLegPos){
    //splitString(content, ':');
    int idLed = splitedString[0].toInt();
    if((!A_ID && A_ID*idLed == 0) || (A_ID && A_ID*idLed != 0)){
      if(A_ID) idLed-=3;
      int listNewPos[NB_ART] = {splitedString[1].toInt(), splitedString[2].toInt(), splitedString[3].toInt()};
      setLegPos(idLed, listNewPos);

      Serial.println("----------------\n");
      for(int i=0; i<NB_SPLIT; i++){
        Serial.println(splitedString[i]);
      }
    }
    newLegPos = false;
  }
}



void setLegPos(int idLeg, int pos[NB_ART]){
  //Set the new pos for all the motor in one leg
  for (int i = 0; i < NB_ART; i++) {
    int angle = i<=1 ? 90-(pos[i]*side) : 90+(pos[i]*side);
    leg[idLeg][2-i].write(angle);
  }
}



void splitString(String data, char separator){
  int lastIndex = -1;
  int indexLastChar = 0;
  for(int i=0; i<NB_SPLIT; i++){
    indexLastChar = data.indexOf(separator, indexLastChar+1);
    if(indexLastChar == -1){
      splitedString[i] = data.substring(lastIndex+1, data.length());
      break;
    }
    splitedString[i] = data.substring(lastIndex+1, indexLastChar);
    lastIndex = indexLastChar;
  }
}



void DataReceive(int numBytes){
  int i=0;
  char data[RESP_SIZE];
  char character;
  memset(data, 0, RESP_SIZE);
  while(Wire.available()){
    character = Wire.read();
    if(character == 'm'){
      newLegPos = true;
    }else if(character == 'e'){
      break;
    }else{
      data[i++]=character;
      //content.concat(character);
      delay(10);
    }
  }
  splitString(String(data), ':');
}
