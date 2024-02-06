#ifndef ServoArm_h
#define ServoArm_h
#include <Arduino.h>
#include <Servo.h>

class ServoArm {
    
    private:

        Servo baseServo;
        Servo shoulderServo;
        Servo elbowServo;
        Servo wristServo;
        Servo gripperServo;
        Servo wristRotateServo;
    
    public:
    
        int initBasePosition = 90;
        int initShoulderPos = 90;
        int initElbowPos = 90;
        int initWristPos = 90;
        int initGripperPos = 90;
        int initWristRPos = 90;
    
        uint8_t basePin, shoulderPin, elbowPin, wristPin, gripperPin, wristRotatePin;
        
        ServoArm(uint8_t basePin = 2, uint8_t shoulderPin = 3, uint8_t elbowPin = 4, uint8_t wristPin = 10, uint8_t gripperPin = 11, uint8_t wristRotatePin = 12);
        void begin();
        void moveBase(int angle, int movSpeed = 35);
        void moveShoulder(int angle, int movSpeed = 35, bool handTracking = false);
        void moveElbow(int angle, int movSpeed = 35);
        void moveWrist(int angle, int movSpeed = 35);
        void moveGripper(int angle, int movSpeed = 35);
        void moveWristR(int angle, int movSpeed = 35);
        void moveAll(int angle, int freq = 1000);
        void getObjectLeft();
};
#endif
