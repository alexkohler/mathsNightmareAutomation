# Math's Nightmare Automation
Automation of Neopet's Math's Nightmare Flash game using PyAutoGui for clicking/keyboard input and Tesseract for optical character recognigition

# Dependencies
Installable via pip:
* pyautogui 
* pytesseract
* pyscreenshot

# Usage
This script is configured to start at the start screen, and will perform division problems. No parameters are required. Simply run *python math.py*. To debug, the images passed to Tesseract are saved in the debugImg directory. The Res directory contains image resources for pyautogui.

Note: This script can be configured to perform "random" problems by changing mode string to "random", however, Tesseract does not recognize the division sign, and often confuses it with plus "+". I have not found a viable solution to solve this.

# About
 **Coordinates are based off of using i3 window manager with game in a vertically split halved window (See "Demo" gif below).** This script can easily be modified for other screen setups. The coordinates are the only thing that needs changed. Function analyzeBubble is used to evaluate each math problem. Function cleanImage is used to remove background "noise" (i.e. anything that isn't the number). Below is a sample cleaned image that is passed to Tesseract:
 
 
![demo gif](debugImg/num1boxNum1-reiter.png)
 
 




# Demo
![demo gif](demo.gif)
