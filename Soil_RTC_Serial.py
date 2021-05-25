# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time # RTC
import busio # Soil
import adafruit_pcf8523 # Soil
from adafruit_seesaw.seesaw import Seesaw

import board

## Soil Setup
i2c_bus = board.I2C()
ss = Seesaw(i2c_bus, addr=0x36)

# Clock setup
# myI2C = busio.I2C(board.SCL, board.SDA)
# rtc = adafruit_pcf8523.PCF8523(myI2C)
# myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(i2c_bus)

while True:
    # Read moisture level through capacitive touch pad
    touch = ss.moisture_read()

    # Read temperature from the temperature sensor
    temp = ss.get_temp()

    # Read datetime
    t = rtc.datetime

    # Print datetime, data
    print("DT: %d/%d/%d  %d:%02d:%02d " % (t.tm_mon, t.tm_mday, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec) +
          "temp: " + str(temp) + "  moisture: " + str(touch))

    # print("temp: " + str(temp) + "  moisture: " + str(touch))
    time.sleep(1)
