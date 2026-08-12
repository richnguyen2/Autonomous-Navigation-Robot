#include "motor_driver.h"

void MotorDriver::begin() {
    pinMode(PIN_STBY, OUTPUT);
    pinMode(PIN_PWM_RIGHT, OUTPUT);
    pinMode(PIN_PWM_LEFT, OUTPUT);
    pinMode(PIN_DIR_RIGHT, OUTPUT);
    pinMode(PIN_DIR_LEFT, OUTPUT);
    stop();
}

void MotorDriver::command_motors(int left_pwm, int right_pwm) {
    digitalWrite(PIN_STBY, HIGH);

    digitalWrite(PIN_DIR_LEFT, (left_pwm >= 0) ? HIGH : LOW);
    digitalWrite(PIN_DIR_RIGHT, (right_pwm >= 0) ? HIGH : LOW);

    int final_left = constrain(abs(left_pwm), 0, 255);
    int final_right = constrain(abs(right_pwm), 0, 255);

    analogWrite(PIN_PWM_LEFT, final_left);
    analogWrite(PIN_PWM_RIGHT, final_right);
}

int MotorDriver::velocity_to_pwm(float lin_vel) const {
    if (lin_vel == 0.0f) return 0;
    float val = (abs(lin_vel) - 0.01f) / 0.0124f; 
    return constrain(static_cast<int>(val), 0, 255);
}

int MotorDriver::angular_to_pwm(float ang_vel) const {
    if (ang_vel == 0.0f) return 0;
    float val = (abs(ang_vel) + 55.8f) / 2.258f;  
    return constrain(static_cast<int>(val), 0, 255);
}

void MotorDriver::stop() {
    digitalWrite(PIN_STBY, LOW);
    analogWrite(PIN_PWM_LEFT, 0);
    analogWrite(PIN_PWM_RIGHT, 0);
}