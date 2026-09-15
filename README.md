# Hand Tracking Test

## Overview

My first python program made to learn the syntax and how python works compared to C# or Java. The project uses OpenCV and NumPy to determine the approximate position of your hand through the device camera. It uses HSV values to determine the interesting parts of the image and masks those parts, using the mask it draws contours around the interesting parts and then determines your palm and your fingertips if your hand is the largest contour in the frame.

It is not perfect and sometimes struggles to pick up on your hand. I find that it works best in a decently lit area with a contrasting background to make your hands stand out.

## Technologies Used

- Python
- OpenCV
- NumPy

## How It Works

Run the program and use the sliders on the Control Screen to narrow down the important parts of the images. Keep an eye on the mask screen until only your hand are on the screen, if your face is also within frame try to ensure that your hand is the largest "object" in the frame so that the project does not accidentally try using a different part to determine the finger positions. This program currently only works with one hand at a time.

## What I Learned

- Python Syntax
- Basics of how Python works
- Basics of how OpenCV works
- Basics of hand tracking concepts and ideas.

## Future Improvements

- Better hand detetion
- AI implementation for more accurate detection
- Draw objects on the screen with specific gestures
