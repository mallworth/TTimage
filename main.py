# TTimage

# This program captures frames from webcam feed and converts them into ASCII art.
# It utilizes OpenCV for webcam access and PIL for image processing.

# Max Allworth-Miles
# January 03, 2024

import cv2
import numpy
from PIL import ImageFont, ImageDraw, Image

capture = cv2.VideoCapture(0)

# Set scaling value to determine # of chars
scale = 0.023

while True:
    # Get frame from webcam feed
    ret, frame = capture.read()

    # Mirror horizontally
    frame = cv2.flip(frame, 1)

    # Get frame dimensions
    height, width, cc = frame.shape

    # Set number of rows and columns
    char_rows = int(width * scale)
    char_columns = int(height * scale)

    # Pass grayscale version of current frame to PIL
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pil_frame = Image.fromarray(rgb_frame)

    # Resize PIL frame to have one pixel per character
    char_squares = pil_frame.resize((char_rows, char_columns))

    # Convert char_squares to list of pixels 
    pixels = list(char_squares.getdata())

    # String of chars for final image
    ttimage = ''

    newline = 0

    for pixel in pixels:
        chars = [(0, ' '), (70, ','), (100, '~'), (150, '*'), (190, '?'), (230, '$'), (245, '#'), (255, '@')]

        # Find correct character for current pixel
        for i in range(0, len(chars) - 1):
                if chars[i][0] <= pixel <= chars[i + 1][0]:
                    ttimage += chars[i][1]
        
        # Insert line break appropriately  
        newline += 1   
        if newline == (char_rows):
            ttimage += '\n'
            newline = 0

    fontsize = 50
    font = ImageFont.truetype("Glass_TTY_VT220.ttf", fontsize)

    # Create black background for text overlay
    background = numpy.zeros((height, height, 3), dtype=numpy.uint8)

    # Pass background to PIL
    pil_background = Image.fromarray(background)

    overlay = ImageDraw.Draw(pil_background)

    overlay.text((0, 0), ttimage, font=font)

    # Pass background with text overlay back to OpenCV
    ttimage_cv2 = numpy.array(pil_background)

    cv2.imshow("TTimage (Press 'q' to quit)", ttimage_cv2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()