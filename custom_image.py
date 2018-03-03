from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI


# Raspberry Pi configuration.
DC = 18
#RST = 23
RST = 16
SPI_PORT = 0
SPI_DEVICE = 0


# Create TFT LCD display class.
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

# Initialize display.
disp.begin()

# Load an image.
print('Loading image...')
image = Image.open('lcd_test.jpg')

# Resize the image and rotate it so it's 240x320 pixels.
image = image.rotate(90).resize((240, 320))

# Draw the image on the display hardware.
print('Drawing image')
#disp.display(image)

#-----------------------------

#PIL Draw object to start drawing on the display buffer.
draw = disp.draw()
                 
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
                                                                                         
# Write two lines of white text on the buffer, rotated degrees counter clockwise.
draw_rotated_text(disp.buffer, 'Dr WiZard', (150, 120), 90, font, fill=(255,0, 0))
draw_rotated_text(disp.buffer, 'IoT Estate Access', (170, 90), 90, font, fill=(0,255,0))
                                                                                             
#Write buffer to display hardware, must be called to make things visible on the
# display!
disp.display(image)
#disp.display()
