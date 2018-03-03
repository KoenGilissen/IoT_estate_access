#!/usr/bin/env python
__author__ = "Dr. Ing. Koen Gilissen"
__version__ = "1.0.0"
__maintainer__ = "Dr. Ing. Koen Gilissen"
__email__ = "gilissenkoen@gmail.com"

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

import random
import logging
import argparse
from sys import stdout
import sys
import signal

#config signal interrupt
def signal_interrupt_handler(signal, frame):
    print '{}{}'.format('\n', 'exiting in style...')
    sys.exit(0)

#register singal handler
signal.signal(signal.SIGINT, signal_interrupt_handler)

# configure default logging
LOG = logging.getLogger('GFX estate')
FORMATTER = logging.Formatter(
	fmt='%(name) 12s|%(levelname) 6s|%(asctime) 20s|%(message)s',
	datefmt='%Y-%m-%d %H:%M:%S')
_SH = logging.StreamHandler(stdout)
_SH.setLevel(logging.DEBUG)
_SH.setFormatter(FORMATTER)
LOG.addHandler(_SH)

# configure an argument parser
parser = argparse.ArgumentParser(description='GFX estate')
parser.add_argument('-d', action='store_true', help='Turn on DEBUG output')
parser.add_argument('-v', action='store_true', help='Turn on INFO output')
args = parser.parse_args()

# configure the log level dynamically
LOG.setLevel(logging.WARN)
if args.v:
	LOG.setLevel(logging.INFO)
if args.d:
	LOG.setLevel(logging.DEBUG)

# Raspberry Pi configuration. 
DC = 18 #GPIO18  PIN12
RST = 23 #GPIO23 PIN16
SPI_PORT = 0
SPI_DEVICE = 0

LOG.debug("DEBUG test")
LOG.info("INFO test")


# Create TFT LCD display class.
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

# Initialize display.
disp.begin()

# Clear the display to a red background.
# Can pass any tuple of red, green, blue values (from 0 to 255 each).
disp.clear((0, 0, 0))


# Get a PIL Draw object to start drawing on the display buffer.
draw = disp.draw()

red = 0
green = 0
blue = 0
lines = 0
x1 = 0
x2 = 319
draw.line((0, 0, 0, 319), fill=(255,255,255))
draw.line((239, 0, 239, 319), fill=(255,255,255))
while True:
    while (lines < 240):
        red = random.randrange(255)
        green = random.randrange(255)
        blue = random.randrange(255)
        LOG.debug("r:%d g:%d b:%d", red, green, blue)
        draw.line((lines, x1, lines, x2), fill=(red, green, blue))
        lines = lines + 1
    
    disp.display()
    lines = 0
    
# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 16)

# Define a function to create rotated text.  Unfortunately PIL doesn't have good
# native support for rotated fonts, but this function can be used to make a
# text image and rotate it so it's easy to paste in the buffer.
def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)

# Write two lines of white text on the buffer, rotated 90 degrees counter clockwise.
draw_rotated_text(disp.buffer, 'Hello World!', (150, 120), 90, font, fill=(255,255,255))
draw_rotated_text(disp.buffer, 'This is a line of text.', (170, 90), 90, font, fill=(255,255,255))

# Write buffer to display hardware, must be called to make things visible on the
# display!
disp.display()
