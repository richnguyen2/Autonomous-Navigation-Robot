#ifndef ULTRASONIC_SENSOR_H
#define ULTRASONIC_SENSOR_H

#include "sensor_interfaces.h"

class UltrasonicSensor final : public DistanceSensorInterface {
  private:
    static constexpr int trigPin = 13;
    static constexpr int echoPin = 12;
  
  public:
    void begin();
    float get_distance();
};

#endif