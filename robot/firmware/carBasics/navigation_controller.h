#ifndef NAVIGATION_CONTROLLER_H
#define NAVIGATION_CONTROLLER_H

#include "sensor_interfaces.h"
#include "motor_driver.h"

enum class NavState {
    IDLE,
    DRIVE_STRAIGHT,
    TURN_IN_PLACE,
};

class NavigationController {
private:
    ImuInterface* imu;
    MotorDriver* motors;
    DistanceSensorInterface* sonar; 

    NavState current_state;
    float target_heading;
    unsigned long maneuver_start_time;
    unsigned long maneuver_duration_ms;

    float base_linear_vel; // base vel of 1.25 ft/s
    
    static constexpr float OBSTACLE_THRESHOLD = 10.0f; // 10 inch

    // Controller Gains
    static constexpr float KP_STRAIGHT = 20.0f;
    static constexpr float KP_TURN = 1.0f;

    // Motor Turn Constraints
    static constexpr int MIN_TURN_PWM = 40;
    static constexpr int MAX_TURN_PWM = 70;

    float total_loop_time_ms;

public:
    NavigationController(ImuInterface* imu_ptr, MotorDriver* motor_ptr, DistanceSensorInterface* sonar_ptr);

    void set_drive_straight(float distance); // Distance in ft
    void set_command_turn(float degrees_to_turn);
    void set_command_stop();

    float NavigationController::p_controller(float current, float desire, float Kp);
    
    void update(NavState new_state, float distance, float);
    NavState get_state() const { return current_state; }
};

#endif