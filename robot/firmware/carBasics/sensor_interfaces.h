#ifndef SENSOR_INTERFACES_H
#define SENSOR_INTERFACES_H

class ImuInterface {
public:
    virtual ~ImuInterface() = default;

    virtual bool initialize() = 0;
    virtual void calibrate() = 0;
    virtual void update() = 0;
    virtual float get_heading() const = 0;
    virtual void reset_heading() = 0;
};

class DistanceSensorInterface {
  public:
    virtual ~DistanceSensorInterface() = default;

    virtual void begin() = 0;
    virtual float get_distance() = 0;
};

#endif