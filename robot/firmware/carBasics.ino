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

void setup() {
  Serial.begin(9600);

  motors.begin();
  imu.initialize();
  imu.calibrate();
  sonar.begin();
  delay(delayTime);
  //nav.update(NavState::TURN_IN_PLACE, 0.0f,-90);
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

int test = 0;

void loop() {
  // No Data, Do nothing
  while (Serial.available() == 0) {

  }
  // Looks for end of line character (carriage return)
  // In python we need to append the special chacter \r at the end of our code
  cmd = Serial.readStringUntil('\r');
  cmd.trim();  // IMPORTANT: removes \r and whitespace

  Serial.println("ACK:" + cmd);  // CONFIRM RECEIVED

  if (cmd == "forward") {
    Serial.print("HEADING:");
    Serial.println(imu.get_heading());
    nav.update(NavState::DRIVE_STRAIGHT, 1.0f, 0);
  }
  if (cmd == "turn_left") {
    nav.update(NavState::TURN_IN_PLACE, 0.0f, -90);
    Serial.print("HEADING:");
    Serial.println(imu.get_heading());
  }
  if (cmd == "turn_right") {
    nav.update(NavState::TURN_IN_PLACE, 0.0f, 90);
    Serial.print("HEADING:");
    Serial.println(imu.get_heading());
  }

  // Stabilization delay. Delay for robot to get to state before using sensor
  delay(50);
  distance = sonar.get_distance();
  sensorFunc(distance);
  delay(100);

  // Done Marker
  Serial.println("DONE");

}