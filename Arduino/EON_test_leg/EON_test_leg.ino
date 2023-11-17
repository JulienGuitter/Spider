#include <Servo.h>

#define NB_LEG    2 //6
#define NB_ART    3

Servo legs[NB_LEG][NB_ART];

const byte legsPin[NB_LEG][NB_ART] = {{13,12,11},
                                      {10,9,8}};

void setup() {
  // put your setup code here, to run once:
  for(int j=0; j<NB_LEG; j++){
    for(int i=0; i<NB_ART; i++){
      legs[j][i].attach(legsPin[j][i]);
      //legs[j][i].write(90);
    }
  }

  Serial.begin(9600);
}

void loop() {
  String content = "";
  char character;
      
  while(Serial.available()) {
       character = Serial.read();
       content.concat(character);
       delay(10);
  }
        
  if (content != "") {
       Serial.print(content);
       int leg = content.substring(0, content.indexOf(":")).toInt();
       int art = content.substring(content.indexOf(":")+1, content.lastIndexOf(":")).toInt();
       int angle = content.substring(content.lastIndexOf(":")+1, content.lastIndexOf("\n")).toInt();
       legs[leg][art].write(angle);

       Serial.println(leg);
       Serial.println(art);
       Serial.println(angle);
       Serial.println();
  }
}
