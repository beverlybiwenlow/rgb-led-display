#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image


image = Image.open("logo.png")

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 16
options.chain_length = 4
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Make image fit our screen.
image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
