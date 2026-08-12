#include "ultrasonic_sensor.h"
#include "mpu6050.h"
#include "motor_driver.h"
#include "navigation_controller.h"
#include "motor_test.h"

int lastExecutionTime = 0;

int delayTime = 1000;

MotorDriver motors;
MPU6050 imu;
UltrasonicSensor sonar;
String cmd;
float distance;

carBase car;

NavigationController nav(&imu, &motors, &sonar);

void forward() {
  nav.update(NavState::DRIVE_STRAIGHT, 1.0f, 0);
}

void left() {
  nav.update(NavState::TURN_IN_PLACE, 0, -90);
}

void right() {
  nav.update(NavState::TURN_IN_PLACE, 0, 90);
}

void testRun(){
  forward();
  left();
  forward();
  right();
  forward();
  right();
  forward();
  right();
  forward();
  forward();
  right();
  forward();
  forward();
}

void setup() {
  Serial.begin(9600);
  Serial.println("Arduino_Started");
  motors.begin();
  imu.initialize();
  imu.calibrate();
  sonar.begin();
  delay(delayTime);
  
  // Wait for arduino to receive GO message before starting
  int start = 0;
  while (start == 0) {
    Serial.println("READY");
    cmd = Serial.readStringUntil('\r');
    cmd.trim();
    if (cmd == "GO") {
      start = 1;
    }
    delay(500);
  }
  
  Serial.println("Commands: ");
  forward();
}

void sensorFunc(float distance) {
  if (distance <= 30) {
    Serial.println("short");
  } else if ((distance > 30) && (distance < 50)) {
    Serial.println("medium");
  } else if (distance >= 50) {
    Serial.println("long");
  } else {
    Serial.println("timeout");
  }
}

void loop() {
}