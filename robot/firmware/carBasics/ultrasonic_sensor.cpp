#include "ultrasonic_sensor.h"
#include <Arduino.h>

// Pin setup
void UltrasonicSensor::begin() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

// Max distance detected with sensor is ~5m
float UltrasonicSensor::get_distance() {
  // Tell sensor to send signal
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long pingTime = pulseIn(echoPin, HIGH, 30000); // returns ping time in microseconds

  float pingSeconds = pingTime / 1000000.0f;
  float distance = (393.0f * 39.3700787f) * pingSeconds; // convert distance to inches
  return distance / 2.0f;
}