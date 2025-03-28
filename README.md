# DOF-GestureRecognition Robot Arm
This project integrates computer vision-based hand tracking with Arduino-controlled servo actuation to create an intuitive gesture-controlled robotic arm. Below is a detailed breakdown of its components, functionality, and technical implementation.

# Overview
The system consists of two main components:

* **Python-based Hand Tracking (Vision System)** – Detects hand gestures using MediaPipe and sends commands via serial communication.
* **Arduino-based Robotic Arm Control (Actuation System)** – Receives serial commands and drives servo motors to move the robotic arm.

**MediaPipe Hand Landmark Detection:**
The system uses MediaPipe’s Hands model to detect 21 key landmarks on a hand (as shown below)

<img src="https://github.com/user-attachments/assets/8bc8294e-d182-4c38-b9d2-73a73890da7a" width=550>

### Gesture Mapping (Finger-to-Thumb Touch Detection)
When a fingertip (index, middle, ring, or pinky) comes within **30 pixels** of the thumb tip, a command is sent to control the robotic arm.

#### Right Hand Controls (Increase Angle)
| Finger        | Landmark ID | Command Sent | Servo Controlled | Movement          |
|---------------|-------------|--------------|-------------------|-------------------|
| **Index**     | 8           | `'b'`        | Base              | Rotate right (+1°)|
| **Middle**    | 12          | `'s'`        | Shoulder          | Lift up (+1°)     |
| **Ring**      | 16          | `'e'`        | Elbow             | Bend down (+1°)   |
| **Pinky**     | 20          | `'w'`        | Wrist             | Tilt up (+1°)     |

#### Left Hand Controls (Decrease Angle)
| Finger        | Landmark ID | Command Sent | Servo Controlled | Movement          |
|---------------|-------------|--------------|-------------------|-------------------|
| **Index**     | 8           | `'h'`        | Base              | Rotate left (-1°) |
| **Middle**    | 12          | `'i'`        | Shoulder          | Lower down (-1°)  |
| **Ring**      | 16          | `'j'`        | Elbow             | Straighten (-1°)  |
| **Pinky**     | 20          | `'k'`        | Wrist             | Tilt down (-1°)   |

Detected fingertips are marked with purple circles.
When a finger touches the thumb, a green line is drawn between them.

# Serial Communication
Uses pyserial to send single-character commands ('b', 's', 'e', etc.) to the Arduino.
Automatically detects the correct COM port (for Arduino) and camera index (for OpenCV).

### Servo Control Logic
- Each servo is controlled via **PWM signals** (Pulse Width Modulation)
- The `ServoArm` class (`Library.ino`) provides smooth movement methods:

```cpp
void moveBase(int angle, int movSpeed = 35);      // Base rotation
void moveShoulder(int angle, int movSpeed = 35);  // Shoulder movement
void moveElbow(int angle, int movSpeed = 35);     // Elbow movement
void moveWrist(int angle, int movSpeed = 35);     // Wrist tilt
void moveGripper(int angle, int movSpeed = 35);   // Gripper open/close
void moveWristR(int angle, int movSpeed = 35);    // Wrist rotation
```

Instead of jumping directly to a target angle, servos move 1° at a time with a configurable delay (movSpeed).
This prevents sudden jerks and reduces mechanical stress.

### Core Python Components
```python
import mediapipe as mp  # Hand landmark detection
import cv2              # Real-time video processing
from google.protobuf.json_format import MessageToDict  # Handedness parsing
```

<img src="https://github.com/user-attachments/assets/180dda2e-1c9c-4ef9-8f40-bf52a44a2ebc" width=400>
<img src="https://github.com/user-attachments/assets/3416d8c4-640a-4ab7-98d5-fdbf2ceef128" width=450 height=450>



