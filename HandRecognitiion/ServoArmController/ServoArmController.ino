#include <ServoArm.h>

int data;
ServoArm servo = new ServoArm();
void setup() {
  
  Serial.begin(9600);
  servo.begin();

}

int baseDegree = servo.initBasePosition;
int shoulderDegree = servo.initShoulderPos;
int elbowDegree = servo.initElbowPos;
int wristDegree = servo.initWristPos;
int gripperDegree = servo.initGripperPos;

void loop() {

  if ( Serial.available() > 0 ) {

    data = Serial.read();
    
    if (data == 'b') {
      servo.moveBase( baseDegree );
      baseDegree++;
    } else if (data == 's') {
      servo.moveShoulder( shoulderDegree, true );
      shoulderDegree++;
    } else if (data == 'e') {
      servo.moveElbow( elbowDegree );
      elbowDegree++;
    } else if (data == 'w') {
      servo.moveWrist( wristDegree );
      wristDegree++;
    } else if (data == 'g') {
      servo.moveGripper( gripperDegree );
      gripperDegree++;
    } else if (data == 'rb') {
      servo.moveBase( baseDegree );
      baseDegree--;
    } else if (data == 'rs') {
      servo.moveShoulder( shoulderDegree );
      shoulderDegree--;
    } else if (data == 're') {
      servo.moveElbow( elbowDegree );
      elbowDegree--;
    } else if (data == 'rw') {
      servo.moveWrist( wristDegree );
      wristDegree--;
    } else if (data == 'rg') {
      servo.moveGripper( gripperDegree );
      gripperDegree--;
    }
  }

}
