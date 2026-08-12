#include "navigation_controller.h"

NavigationController::NavigationController(ImuInterface* imu_ptr, MotorDriver* motor_ptr, DistanceSensorInterface* sonar_ptr)
    : imu(imu_ptr), motors(motor_ptr), sonar(sonar_ptr), 
      current_state(NavState::IDLE), target_heading(0.0f), 
      maneuver_start_time(0), maneuver_duration_ms(0), base_linear_vel(1.25f), total_loop_time_ms(0.0f) {}


// drive straight setter to set the target heading, open loop time control for distance, and current state
void NavigationController::set_drive_straight(float distance) {
    target_heading = imu->get_heading();
    maneuver_duration_ms = static_cast<unsigned long>((distance / base_linear_vel) * 1000.0f);
    maneuver_start_time = millis();
    current_state = NavState::DRIVE_STRAIGHT;
}

// turn setter to set the target heading, and current state
void NavigationController::set_command_turn(float degrees_to_turn) {
    target_heading = imu->get_heading() + degrees_to_turn;
    current_state = NavState::TURN_IN_PLACE;
}

// stop setter to set current state
void NavigationController::set_command_stop() {
    current_state = NavState::IDLE;
}

// P controller for movement
float NavigationController::p_controller(float current, float desired, float Kp) {
    float error = desired - current;
    Serial.print(error);
    Serial.print(",");
    float correction = Kp * error;
    return correction;
}

void NavigationController::update(NavState new_state, float distance, float degrees_to_turn) {
    
    // Establish the state parameters: state, time duration, heading target
    if (new_state == NavState::DRIVE_STRAIGHT) {
        set_drive_straight(distance);
    } else if (new_state == NavState::TURN_IN_PLACE) {
       set_command_turn(degrees_to_turn); 
    } else {
        set_command_stop();
    }

    // set base speed
    int base_pwm = motors->velocity_to_pwm(base_linear_vel);

    // control loop
    while (current_state == new_state) {
        unsigned long loop_start = micros();

        // Update readings for the IMU
        imu->update();

        float current_heading = imu->get_heading();
        float obstacle_dist = sonar->get_distance();
    
        // State Machine
        if (current_state == NavState::DRIVE_STRAIGHT) {
            
            // Distance control is open-loop
            if ((millis() - maneuver_start_time) >= maneuver_duration_ms) {
                set_command_stop();
                motors->stop();
                Serial.println("Cmd Straight Done!");
                break;
            }

            // Closed-loop heading correction
            float corr = p_controller(current_heading, target_heading, KP_STRAIGHT);

            int left_pwm = static_cast<int>(base_pwm + corr);
            int right_pwm = static_cast<int>(base_pwm - corr);
    
            motors->command_motors(left_pwm, right_pwm);

        } else if (current_state == NavState::TURN_IN_PLACE){
            float error = target_heading - current_heading;
            
            // Turn until error tolerance is reached
            if (abs(error) <= 0.3f) {
                set_command_stop();
                motors->stop();
                Serial.println("Cmd Turn Done!");
                break;
            } else {
                
                //float corr = pd_controller(current_heading, target_heading, KP_TURN, KD_TURN, dt, previous_error);
                float corr = p_controller(current_heading, target_heading, KP_TURN);

                int spin_pwm = MIN_TURN_PWM + abs(corr);
                
                // Limit speed to prevent slippage and minimum voltage for motor
                spin_pwm = constrain(spin_pwm, MIN_TURN_PWM, MAX_TURN_PWM);
                
                // Turn based on error direction
                if (error > 0) {
                    motors->command_motors(spin_pwm, -spin_pwm); // Turn Right
                } else {
                    motors->command_motors(-spin_pwm, spin_pwm); // Turn Left
                }
                
            }
        } else if (current_state == NavState::IDLE) {
            motors->stop();
            Serial.println("Cmd Stop!");
            break;
        }
        unsigned long loop_end = micros();
        float loop_time_ms = (loop_end - loop_start) / 1000.0;
        total_loop_time_ms += loop_time_ms;
        Serial.print(target_heading);
        Serial.print(",");
        Serial.print(current_heading);
        Serial.print(",");
        Serial.println(total_loop_time_ms); 
    }
}