#ifndef MOTOR_DRIVER_H
#define MOTOR_DRIVER_H

#include <Arduino.h>

class MotorDriver final {
private:
    static constexpr int PIN_STBY = 3;     
    static constexpr int PIN_PWM_RIGHT = 5; 
    static constexpr int PIN_DIR_RIGHT = 7; 
    static constexpr int PIN_PWM_LEFT = 6;  
    static constexpr int PIN_DIR_LEFT = 8;  

public:
    MotorDriver() = default;

    void begin();
    void command_motors(int left_pwm, int right_pwm);
    int velocity_to_pwm(float lin_vel) const;
    int angular_to_pwm(float ang_vel) const;
    void stop();
};

#endif