#  Startup screen for Anthropocene project

import time
import subprocess
import datetime
import os

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# font sizes
font_big = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf', 16)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf', 12)
 
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

def show_OLED_message(text, text2):

    # Write three lines of text. Two are passed to it.

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    draw.text((x, top+8), str(datetime.datetime.now()), font=font, fill=255)
    draw.text((x, top+16), text, font=font, fill=255)
    draw.text((x, top+25), text2, font=font, fill=255)

    disp.image(image)
    disp.show()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

# display public IP
# f = os.popen('curl ifconfig.me')

# display private IP
