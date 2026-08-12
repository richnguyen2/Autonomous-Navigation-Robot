#include "mpu6050.h"
#include <Arduino.h>
#include <Wire.h>
#include <math.h>

bool MPU6050::initialize() {
  Wire.begin();
  uint8_t chip_id = 0x00;
  uint8_t cout = 0;
  do
  {
    chip_id = getDeviceID();
    delay(10);
    cout += 1;
    if (cout > 10)
    {
      return false;
    }
  } while (chip_id == 0X00 || chip_id == 0XFF);
  setClockSource(MPU6050_CLOCK_PLL_XGYRO);
  setFullScaleGyroRange(MPU6050_GYRO_FS_250);
  setFullScaleAccelRange(MPU6050_ACCEL_FS_2);
  setSleepEnabled(false);
  return true;
}

void MPU6050::calibrate() {
  unsigned short times = 100;
  for (int i = 0; i < times; i++)
  {
    gz = getRotationZ();
    gzo += gz;
  }
  gzo /= times;
}

void MPU6050::update() {
  unsigned long now = millis();
  dt = (now - lastTime) / 1000.0;
  lastTime = now;
  gz = getRotationZ();
  float gyroz = -(gz - gzo) / 131.0 * dt;
  if (fabs(gyroz) < 0.05)
  {
    gyroz = 0.00;
  }
  current_heading += gyroz;
}

void MPU6050::setClockSource(uint8_t source) {
  I2Cdev::writeBits(MPU6050_DEFAULT_ADDRESS, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_CLKSEL_BIT,
                    MPU6050_PWR1_CLKSEL_LENGTH, source);
}

void MPU6050::setSleepEnabled(bool enabled) {
  I2Cdev::writeBit(MPU6050_DEFAULT_ADDRESS, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT,
                   enabled);
}

void MPU6050::setFullScaleGyroRange(uint8_t range) {
  I2Cdev::writeBits(MPU6050_DEFAULT_ADDRESS, MPU6050_RA_GYRO_CONFIG, MPU6050_GCONFIG_FS_SEL_BIT,
                    MPU6050_GCONFIG_FS_SEL_LENGTH, range);
}

void MPU6050::setFullScaleAccelRange(uint8_t range) {
  I2Cdev::writeBits(MPU6050_DEFAULT_ADDRESS, MPU6050_RA_ACCEL_CONFIG,
                    MPU6050_ACONFIG_AFS_SEL_BIT, MPU6050_ACONFIG_AFS_SEL_LENGTH,
                    range);
}

uint8_t MPU6050::getDeviceID() {
  I2Cdev::readBits(MPU6050_DEFAULT_ADDRESS, MPU6050_RA_WHO_AM_I, MPU6050_WHO_AM_I_BIT,
                   MPU6050_WHO_AM_I_LENGTH, buffer);
  return buffer[0];
}

int16_t MPU6050::getRotationZ() {
  I2Cdev::readBytes(MPU6050_DEFAULT_ADDRESS, MPU6050_RA_GYRO_ZOUT_H, 2, buffer);
  return (((int16_t)buffer[0]) << 8) | buffer[1];
}