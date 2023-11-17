#include <Servo.h>

#define NB_ART        3
#define NB_ANIM       1
#define NB_STEP_ANIM  4
#define NB_LEG_MOTOR  3
#define NB_LEGS       6

Servo leg[NB_LEGS][NB_ART];

const byte legsPin[NB_LEGS][NB_ART] = {{11, 12, 13}, {8, 9, 10}, {5,6,7}, {2,3,4}, {14,15,16}, {17,18,19}}; //{11, 12, 13}, {8, 9, 10}, {5,6,7}, {2,3,4}, {14,15,16}, {17,18,19}
bool anim = false;
int stepAnim = 0;

int startPos[NB_ART] = {-20, 90, 10};

int listAnim[NB_ANIM][NB_STEP_ANIM][NB_LEG_MOTOR] = {{{-40,0,-20},
                                                      {-40,30,20},
                                                      {-10,30,20},
                                                      {-10,0,-20}}};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int j=0; j<NB_LEGS; j++){
    for (int i = 0; i < NB_ART; i++) {
      leg[j][i].attach(legsPin[j][i]);
      int side = j%2 ? 1 : -1;
      int angle = i<=1 ? 90-(startPos[i]*side) : 90+(startPos[i]*side);
      leg[j][i].write(angle);
      Serial.println(angle);
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  char character;

  while (Serial.available()) {
    character = Serial.read();
    if (character == 's' && !anim) {
      anim = true;
      stepAnim = 0;
    }
    if (character == 'p' && anim) {
      anim = false;
    }
  }

  if (anim) {
    for(int j=0; j<NB_LEGS; j++){
      setLegPos(j, listAnim[0][stepAnim]);
      /*
      for (int i = 0; i < NB_ART; i++) {
        leg[j][2-i].write(listAnim[0][stepAnim][i]);
        Serial.println(listAnim[0][stepAnim][i]);
      }
      */
    }
    Serial.println();
    
    stepAnim++;
    if(stepAnim == NB_STEP_ANIM){
      stepAnim=0;
    }
    //anim = stepAnim == NB_STEP_ANIM ? 0 : anim;
    delay(500);
  }
}

void setLegPos(int idLeg, int pos[NB_ART]){
  //Set the new pos for all the motor in one leg
  for (int i = 0; i < NB_ART; i++) {
    int side = idLeg%2 ? 1 : -1;
    int angle = i<=1 ? 90-(pos[i]*side) : 90+(pos[i]*side);
    leg[idLeg][2-i].write(angle);
    //Serial.println(pos[i]);
  }
}

/*

init: R:-20 , M:90 , B:10

1: R:-20 , M:0 , B:-40
2: R:20 , M:0 , B:-40
3: R:20 , M:30 , B:-10
4: R:-20 , M:30 , B:-10


*/