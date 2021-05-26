# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Set up stand alone version
import board

import time # RTC

import busio # Soil
import adafruit_pcf8523 # Soil
from adafruit_seesaw.seesaw import Seesaw

import displayio
import terminalio
# can try import bitmap_label below for alternative
from adafruit_display_text import label
import adafruit_displayio_sh1107


## Soil Setup
i2c_bus = board.I2C()
ss = Seesaw(i2c_bus, addr=0x36)

# Clock setup
rtc = adafruit_pcf8523.PCF8523(i2c_bus)

# Screen setup
displayio.release_displays()
display_bus = displayio.I2CDisplay(i2c_bus, device_address=0x3C)
WIDTH = 128 # SH1107 is vertically oriented 64x128
HEIGHT = 64
BORDER = 2

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

display.auto_refresh = True

# Note above, could not just merge rtc and soil scripts. They call/addr i2c differnetly
# But if we just point RTC at soil setup , that works.

while True:
    # Read moisture level through capacitive touch pad
    touch = ss.moisture_read()

    # Read temperature from the temperature sensor
    temp = ss.get_temp()

    # Read datetime
    t = rtc.datetime

    # Print datetime, data
    #print("%d/%d/%d  %d:%02d:%02d " % (t.tm_mon, t.tm_mday, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec) +
    #      "temp: " + str(temp) + "  moisture: " + str(touch))

    # print("temp: " + str(temp) + "  moisture: " + str(touch))

    ## Print to screen
    text1 = "Soil Moisture:"
    text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, scale=1, x=8, y=15)
    splash.append(text_area)

    # Draw a smaller inner rectangle in black
    inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(
        inner_bitmap, pixel_shader=inner_palette, x=8, y=25
    )
    splash.append(inner_sprite)


    data_area = label.Label(terminalio.FONT, text=str(touch), color=0xFFFFFF, scale=2, x=15, y=40)
    splash.append(data_area)

    time.sleep(2)
