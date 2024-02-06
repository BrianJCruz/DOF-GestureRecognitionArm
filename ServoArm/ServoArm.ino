#include <Servo.h>

const int basePin = 2;
const int shoulderPin = 3;
const int elbowPin = 4;
const int wristPin = 10;
const int gripperPin = 11;
const int wristRotatePin = 12;

int initBasePosition = 90;
int initShoulderPos = 90;
int initElbowPos = 90;
int initWristPos = 90;
int initGripperPos = 90;
int initWristRPos = 90;

Servo baseServo;
Servo shoulderServo;
Servo elbowServo;
Servo wristServo;
Servo gripperServo;
Servo wristRotateServo;

void moveBase(int angle, int movSpeed = 35) {

   if (angle >= initBasePosition) {
     for ( int pos = initBasePosition; pos <= angle; pos += 1 ) {
      baseServo.write(pos);
      delay(movSpeed);
     }
    
   } else if (angle <= initBasePosition) {  
       for ( int pos = initBasePosition; pos >= angle; pos -= 1 ) {     
        baseServo.write(pos);
        delay(movSpeed);
      }
   }

   initBasePosition = angle;
  
}

void moveShoulder(int angle, int movSpeed = 35) {

   if (angle >= initShoulderPos) {
     for ( int pos = initShoulderPos; pos <= angle; pos += 1 ) {
      shoulderServo.write(pos);
      delay(movSpeed);
     }
    
   } else if (angle <= initShoulderPos) {  
       for ( int pos = initShoulderPos; pos >= angle; pos -= 1 ) {     
        shoulderServo.write(pos);
        delay(movSpeed);
      }
   }

   initShoulderPos = angle;
}

void moveElbow(int angle, int movSpeed = 35) {

   if (angle >= initElbowPos) {
     for ( int pos = initElbowPos; pos <= angle; pos += 1 ) {
      elbowServo.write(pos);
      delay(movSpeed);
     }
    
   } else if (angle <= initElbowPos) {  
       for ( int pos = initElbowPos; pos >= angle; pos -= 1 ) {     
        elbowServo.write(pos);
        delay(movSpeed);
      }
   }

   initElbowPos = angle;
}

void moveWrist(int angle, int movSpeed = 35) {

   if (angle >= initWristPos) {
     for ( int pos = initWristPos; pos <= angle; pos += 1 ) {
      wristServo.write(pos);
      delay(movSpeed);
     }
    
   } else if (angle <= initWristPos) {  
       for ( int pos = initWristPos; pos >= angle; pos -= 1 ) {     
        wristServo.write(pos);
        delay(movSpeed);
      }
   }

   initWristPos = angle;
}

void moveGripper(int angle, int movSpeed = 35) {

   if (angle >= initGripperPos) {
     for ( int pos = initGripperPos; pos <= angle; pos += 1 ) {
      gripperServo.write(pos);
      delay(movSpeed);
     }
    
   } else if (angle <= initGripperPos) {  
       for ( int pos = initGripperPos; pos >= angle; pos -= 1 ) {     
        gripperServo.write(pos);
        delay(movSpeed);
      }
   }

   initGripperPos = angle;
}

void moveWristR(int angle, int movSpeed = 35) {

   if (angle >= initWristRPos) {
     for ( int pos = initWristRPos; pos <= angle; pos += 1 ) {
      wristRotateServo.write(pos);
      delay(movSpeed);
     }
    
   } else if (angle <= initWristRPos) {  
       for ( int pos = initWristRPos; pos >= angle; pos -= 1 ) {     
        wristRotateServo.write(pos);
        delay(movSpeed);
      }
   }

   initWristRPos = angle;
}

void moveAll(int angle, int freq = 1000) {
    
  moveBase(angle);
  delay(freq);
  moveShoulder(angle);
  delay(freq);
  moveElbow(angle);
  delay(freq);
  moveWrist(angle);
  delay(freq);
  moveGripper(angle);
  delay(freq);
  moveWristR(angle);
  
  
}

void getObjectLeft(){

  moveBase(40);
  delay(1000);
  moveElbow(100);
  delay(1000);
  moveWrist(35);
  delay(1000);
  moveGripper(10);
  delay(1000);
  moveShoulder(60);
  delay(1000);
  moveGripper(90);
  delay(1000);
  moveShoulder(90);
  delay(1000);
  moveBase(90);
  delay(1000);
  moveShoulder(60);
  delay(1000);
  moveGripper(0);
  delay(1000);
  moveShoulder(90);
  delay(1000);
  moveAll(90);
  delay(1000);
  
  
}


void setup() {

  Serial.begin(19200);
  baseServo.attach(basePin);
  shoulderServo.attach(shoulderPin);
  elbowServo.attach(elbowPin);
  wristServo.attach(wristPin);
  gripperServo.attach(gripperPin);
  wristRotateServo.attach(wristRotatePin);

  moveAll(90);
}

int data;
int baseDegree = 90;
int shoulderDegree = 90;
int elbowDegree = 90;
int wristDegree = 90;
int gripperDegree = 90;

void loop() {
  if ( Serial.available() > 0 ) {

      data = Serial.read();
      
      if (data == 'b') {

        baseServo.write( baseDegree );
        delay(35);
        baseDegree++;

      } else if (data == 's') {

        shoulderServo.write( shoulderDegree );
        delay(35);
        shoulderDegree++;

      } else if (data == 'e') {

        elbowServo.write( elbowDegree );
        delay(35);
        elbowDegree++;

      } else if (data == 'w') {

        wristServo.write( wristDegree );
        delay(35);
        wristDegree++;

      } else if (data == 'g') {

        gripperServo.write( gripperDegree );
        delay(35);
        gripperDegree++;

      } else if (data == 'h') {
        
        Serial.write(data);
        baseServo.write( baseDegree );
        delay(35);
        baseDegree--;

      } else if (data == 'i') {

        shoulderServo.write( shoulderDegree );
        delay(35);
        shoulderDegree--;

      } else if (data == 'j') {

        elbowServo.write( elbowDegree );
        delay(35);
        elbowDegree--;

      } else if (data == 'k') {
        
        wristServo.write( wristDegree );
        delay(35);
        wristDegree--;
      
      } else if (data == 'l') {
      
        gripperServo.write( gripperDegree );
        delay(35);
        gripperDegree--;
      
      }
    }
}

