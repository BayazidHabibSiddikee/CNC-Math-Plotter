#include <ESP32Servo.h>

/**
 * CNC Plotter Controller V2 (Serial Mode)
 * Hardware: ESP32 + MG996R Continuous Rotation Servos
 * Wheel Diameter: 6.7 cm
 * 
 * Low Frequency Mode: 30Hz PWM to reduce mechanical stress.
 * Power Limit: Restricted swing for safer operation with large wheels.
 */

// ==================== CONFIGURATION ====================
Servo motorX;
Servo motorY;

const int PIN_X = 18;
const int PIN_Y = 19;

// HARDWARE CALIBRATION
// Diameter: 6.7cm -> Circumference: 21.05cm
// Speed @ 6V: ~0.9s per rev -> 23.39 cm/s
// Constant: 1000 / 23.39 = 42.75 ms/cm
const float MS_PER_CM_X = 42.75; 
const float MS_PER_CM_Y = 42.75; 

float currentX = 0.0;
float currentY = 0.0;

// Neutral pulse (adjust if your motors creep while stopped)
const int STOP_VAL = 92;   

// Low power limit (0-90). 25 is approx 28% power.
const int MAX_POWER_SWING = 25; 

// ==================== MOTOR LOGIC ====================

void stopMotors() {
  motorX.write(STOP_VAL);
  motorY.write(STOP_VAL);
}

/**
 * Move to target coordinates using proportional power for straight lines.
 */
void moveTo(float targetX, float targetY, float speedFactor) {
  float deltaX = targetX - currentX;
  float deltaY = targetY - currentY;

  float timeX = fabs(deltaX) * MS_PER_CM_X;
  float timeY = fabs(deltaY) * MS_PER_CM_Y;

  // Find dominant axis for timing
  unsigned long T = (timeX >= timeY) ? (unsigned long)timeX : (unsigned long)timeY;
  
  if (T == 0) {
    Serial.println("OK");
    return;
  }

  // Speed adjustment
  T = T / speedFactor;
  if (T < 1) T = 1;

  // Power compensation for the lower MAX_POWER_SWING
  // This ensures the delay matches the slower physical rotation
  float powerCorrection = 88.0 / (float)MAX_POWER_SWING;
  unsigned long correctedT = T * powerCorrection;

  // Calculate speed factors for linear interpolation
  float factorX = timeX / (float)T;
  float factorY = timeY / (float)T;
  if (factorX > 1.0) factorX = 1.0;
  if (factorY > 1.0) factorY = 1.0;

  // Set Motor X
  if (deltaX >= 0) motorX.write(STOP_VAL + (int)(MAX_POWER_SWING * factorX + 0.5));
  else             motorX.write(STOP_VAL - (int)(MAX_POWER_SWING * factorX + 0.5));

  // Set Motor Y
  if (deltaY >= 0) motorY.write(STOP_VAL + (int)(MAX_POWER_SWING * factorY + 0.5));
  else             motorY.write(STOP_VAL - (int)(MAX_POWER_SWING * factorY + 0.5));

  // Block until movement is complete
  delay(correctedT);
  stopMotors();

  currentX = targetX;
  currentY = targetY;
  
  // Signal completion back to the Python controller
  Serial.println("OK"); 
}

// ==================== CORE ====================

void setup() {
  Serial.begin(115200);
  
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  
  // Initialize servos with 30Hz Low Frequency Mode
  motorX.setPeriodHertz(30);
  motorY.setPeriodHertz(30);
  
  motorX.attach(PIN_X, 500, 2400);
  motorY.attach(PIN_Y, 500, 2400);
  
  stopMotors();
  Serial.println("CNC V2 Online | Calibrated: 6.7cm Wheels | Mode: LowFreq");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    
    // Process G1 command: G1 X[val] Y[val] S[speed]
    if (cmd.startsWith("G1")) {
      float x = currentX, y = currentY, s = 1.0;
      
      int xIdx = cmd.indexOf('X');
      int yIdx = cmd.indexOf('Y');
      int sIdx = cmd.indexOf('S');
      
      if (xIdx != -1) {
          int end = (yIdx != -1) ? yIdx : ((sIdx != -1) ? sIdx : cmd.length());
          x = cmd.substring(xIdx + 1, end).toFloat();
      }
      if (yIdx != -1) {
          int end = (sIdx != -1) ? sIdx : cmd.length();
          y = cmd.substring(yIdx + 1, end).toFloat();
      }
      if (sIdx != -1) {
          s = cmd.substring(sIdx + 1).toFloat();
      }
      
      moveTo(x, y, s);
    }
  }
}
