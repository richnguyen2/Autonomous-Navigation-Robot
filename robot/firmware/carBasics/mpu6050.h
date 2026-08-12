#include <I2Cdev.h>

#ifndef MPU6050_H
#define MPU6050_H

#include "sensor_interfaces.h"
#include "I2Cdev.h"

#define MPU6050_ADDRESS_AD0_LOW         0x68
#define MPU6050_DEFAULT_ADDRESS         MPU6050_ADDRESS_AD0_LOW
#define MPU6050_CLOCK_PLL_XGYRO         0x01
#define MPU6050_GYRO_FS_250             0x00
#define MPU6050_ACCEL_FS_2              0x00
#define MPU6050_RA_PWR_MGMT_1           0x6B
#define MPU6050_PWR1_SLEEP_BIT          6
#define MPU6050_PWR1_CLKSEL_BIT         2
#define MPU6050_PWR1_CLKSEL_LENGTH      3
#define MPU6050_RA_GYRO_CONFIG          0x1B
#define MPU6050_GCONFIG_FS_SEL_BIT      4
#define MPU6050_GCONFIG_FS_SEL_LENGTH   2
#define MPU6050_RA_ACCEL_CONFIG         0x1C
#define MPU6050_ACONFIG_AFS_SEL_BIT     4
#define MPU6050_ACONFIG_AFS_SEL_LENGTH  2
#define MPU6050_RA_WHO_AM_I             0x75
#define MPU6050_WHO_AM_I_BIT            6
#define MPU6050_WHO_AM_I_LENGTH         6
#define MPU6050_RA_GYRO_ZOUT_H          0x47

class MPU6050 final : public ImuInterface {
  private:
    float current_heading = 0.0f;
    float gyro_z_offset = 0.0f;

    int16_t gz;
    unsigned long now, lastTime = 0;
    float dt;
    float agz = 0;
    long gzo = 0;

    uint8_t buffer[14];

    void setClockSource(uint8_t source);
    void setFullScaleGyroRange(uint8_t range);
    void setFullScaleAccelRange(uint8_t range);
    void setSleepEnabled(bool enabled);
    uint8_t getDeviceID();
    int16_t getRotationZ();

  public:
    bool initialize();
    void calibrate();
    void update();
    float get_heading() const { return current_heading; }

    void reset_heading() { current_heading = 0.0f; }
};

#endif