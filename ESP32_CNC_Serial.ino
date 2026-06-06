#include <ESP32Servo.h>

// ==================== SERVO & PLOTTER SETUP ====================
Servo motorX;
Servo motorY;

const int PIN_X = 18;
const int PIN_Y = 19;

// HARDWARE CALIBRATION: 6.7cm Wheels + MG996R
// Math: 21.05 cm/rotation | 23.39 cm/s | 42.75 ms/cm
const float MS_PER_CM_X = 42.75; 
const float MS_PER_CM_Y = 42.75; 

float currentX = 0.0;
float currentY = 0.0;
const int STOP_VAL = 92;   // neutral servo pulse

// LOW FREQUENCY POWER LIMIT
const int MAX_POWER_SWING = 25; 

void stopMotors() {
  motorX.write(STOP_VAL);
  motorY.write(STOP_VAL);
}

void moveTo(float targetX, float targetY, float speedFactor) {
  float deltaX = targetX - currentX;
  float deltaY = targetY - currentY;

  float timeX = fabs(deltaX) * MS_PER_CM_X;
  float timeY = fabs(deltaY) * MS_PER_CM_Y;

  unsigned long T = (timeX >= timeY) ? (unsigned long)timeX : (unsigned long)timeY;
  
  if (T == 0) {
    Serial.println("OK");
    return;
  }

  T = T / speedFactor;
  if (T < 1) T = 1;

  // Since we reduced power swing, we must increase the wait time proportionally
  float powerCorrection = 88.0 / (float)MAX_POWER_SWING;
  unsigned long correctedT = T * powerCorrection;

  float factorX = timeX / (float)T;
  float factorY = timeY / (float)T;
  if (factorX > 1.0) factorX = 1.0;
  if (factorY > 1.0) factorY = 1.0;

  if (deltaX >= 0) motorX.write(STOP_VAL + (int)(MAX_POWER_SWING * factorX + 0.5));
  else             motorX.write(STOP_VAL - (int)(MAX_POWER_SWING * factorX + 0.5));

  if (deltaY >= 0) motorY.write(STOP_VAL + (int)(MAX_POWER_SWING * factorY + 0.5));
  else             motorY.write(STOP_VAL - (int)(MAX_POWER_SWING * factorY + 0.5));

  delay(correctedT);
  stopMotors();

  currentX = targetX;
  currentY = targetY;
  Serial.println("OK"); 
}

void setup() {
  Serial.begin(115200);
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  
  // LOW PWM FREQUENCY (30Hz)
  motorX.setPeriodHertz(30);
  motorY.setPeriodHertz(30);
  
  motorX.attach(PIN_X, 500, 2400);
  motorY.attach(PIN_Y, 500, 2400);
  stopMotors();
  Serial.println("ESP32 CNC Ready (Low Frequency Mode)");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    if (cmd.startsWith("G1")) {
      float x = currentX, y = currentY, s = 1.0;
      int xIdx = cmd.indexOf('X');
      int yIdx = cmd.indexOf('Y');
      int sIdx = cmd.indexOf('S');
      
      if (xIdx != -1) x = cmd.substring(xIdx + 1, yIdx != -1 ? yIdx : (sIdx != -1 ? sIdx : cmd.length())).toFloat();
      if (yIdx != -1) y = cmd.substring(yIdx + 1, sIdx != -1 ? sIdx : cmd.length())).toFloat();
      if (sIdx != -1) s = cmd.substring(sIdx + 1).toFloat();
      
      moveTo(x, y, s);
    }
  }
}
