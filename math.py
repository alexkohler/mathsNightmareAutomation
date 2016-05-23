#! python3
# -*- coding: utf-8 -*-
"""
Math's nightmare
	Settings:
	medium quality/regular in a new window, i3 wm with game in LHS halved window
	Extra time given at end of round 4 and round 7
"""

import Image
import pytesseract
import pyautogui
import pyscreenshot as ImageGrab
import logging
import sys
import time



#Filters image to remove background noise and leave only the number
def cleanImage(img):
		pixdata = img.load()
		for y in xrange(img.size[1]):
		    for x in xrange(img.size[0]):
		        #print(pixdata[x, y])
		        if pixdata[x, y][1] > 90: 
		            pixdata[x, y] = (255, 255, 255, 255)
		        if pixdata[x, y][0] == 117: 
		            pixdata[x, y] = (255, 255, 255, 255)
		return img

def analyzeBubble(startingX, startingY, boxNum):
	mode = "div" #random"
	try:
		#grab first number
		im=ImageGrab.grab(bbox=(startingX,startingY,startingX + 37,startingY + 16)) # X1,Y1,X2,Y2
		im = cleanImage(im)
		im.save('debugImg/num1' + 'boxNum' + str(boxNum) + '.png')
		num1=pytesseract.image_to_string(im, config='-psm 8 digits').replace(" ", "").replace("-", "").replace(".", "")

		#grab operator guess if we're doing random (otherwise will default to division)
		if mode == "random":
			im=ImageGrab.grab(bbox=(startingX,startingY,startingX + 60, startingY + 22)) # X1,Y1,X2,Y2
			im = cleanImage(im)
			im.save('debugImg/op' + 'boxNum' + str(boxNum) + '.png')
			opGuess = pytesseract.image_to_string(im, config='-psm 6')
			print('opguess is ' + opGuess)
			op = ""
			if "x" in opGuess.lower():
				op = "mult"	
			elif "+" in opGuess:
				op = "add"	



		#grab second number
		im=ImageGrab.grab(bbox=(startingX,startingY + 21,startingX + 37,startingY + 21 + 18)) # X1,Y1,X2,Y2
		pixdata = im.load()
		im=cleanImage(im)
		im.save('debugImg/num2' + 'boxNum' + str(boxNum) + '.png')
		num2=pytesseract.image_to_string(im, config='-psm 8 digits').replace(" ", "").replace("-", "").replace(".", "")


		# compute result (division)
		if mode == "div":
			result=int(num1) / int(num2)
			logging.debug('bnum %s performed following calculation: %s * %s = %d', boxNum, num1, num2, result)
			pyautogui.click(startingX + 23, startingY + 55)
			pyautogui.typewrite(str(result), interval=0.01)
			im = pyautogui.screenshot()
			pix = im.getpixel((startingX + 23, startingY + 55))
			if pix != (175, 193, 221):
				logging.debug('Correct calculation %d %d %d', pix[0], pix[1], pix[2])
			else:
				# attempt to fix bad calculation
				logging.debug('INCORRECT calculation %d %d %d', pix[0], pix[1], pix[2])
				logging.debug('Incorrect calculation, taking corrective measures')
				im=ImageGrab.grab(bbox=(startingX,startingY-5,startingX + 37,startingY + 20)) # X1,Y1,X2,Y2
				im = cleanImage(im)
				im.save('debugImg/num1' + 'boxNum' + str(boxNum) + '-reiter.png')
				num1=pytesseract.image_to_string(im, config='-psm 8 digits').replace(" ", "").replace("-", "").replace(".", "")
				result=int(num1) / int(num2)
				logging.debug('new guess: bnum %s performed following calculation: %s * %s = %d', boxNum, num1, num2, result)
				pyautogui.click(startingX + 23, startingY + 55)
				pyautogui.typewrite(str(result), interval=0.01)

		# compute result (random mode)
		elif mode == "random":
			if op == "mult":
				result=int(num1) * int(num2)
				logging.debug('bnum %s performed following calculation: %s * %s = %d', boxNum, num1, num2, result)
				pyautogui.click(startingX + 23, startingY + 55)
				pyautogui.typewrite(str(result), interval=0.01)
			elif op == "add":
				result=int(num1) + int(num2)
				logging.debug('bnum %s performed following calculation: %s + %s = %d', boxNum, num1, num2, result)
				pyautogui.click(startingX + 23, startingY + 55)
				pyautogui.typewrite(str(result), interval=0.01)
				im = pyautogui.screenshot()
				if im.getpixel((startingX + 23, startingY + 55))!= (175, 193, 221):
					result=int(num1) / int(num2)
					pyautogui.press('backspace')
					pyautogui.press('backspace')
					pyautogui.press('backspace')
					pyautogui.press('backspace')
					pyautogui.typewrite(str(result), interval=0.01)
			else:
				result=int(num1) / int(num2)
				logging.debug('bnum %s performed following calculation: %s * %s = %d', boxNum, num1, num2, result)
				pyautogui.click(startingX + 23, startingY + 55)
				pyautogui.typewrite(str(result), interval=0.01)
				im = pyautogui.screenshot()
				if im.getpixel((startingX + 23, startingY + 55))!= (175, 193, 221):
					result=int(num1) - int(num2)
					pyautogui.press('backspace')
					pyautogui.press('backspace')
					pyautogui.press('backspace')
					pyautogui.press('backspace')
					pyautogui.typewrite(str(result), interval=0.01)
				im = pyautogui.screenshot()
				if im.getpixel((startingX + 23, startingY + 55))!= (175, 193, 221):
					result=int(num1) + int(num2)
					pyautogui.press('backspace')
					pyautogui.press('backspace')
					pyautogui.press('backspace')
					pyautogui.press('backspace')
					pyautogui.typewrite(str(result), interval=0.01)
			
	except Exception: #swallow exception. The show must go on!
		pass
		return



#logging.disable(logging.DEBUG) # uncomment to block debug log messages
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
try:
	#initialize game setup
	startButton = pyautogui.locateOnScreen('res/startGame.png')
	pyautogui.click(startButton[0]+20, startButton[1])
	time.sleep(1)
	#select division
	div = pyautogui.locateOnScreen('res/div.png')
	pyautogui.click(div[0]+50, div[1]+5)
	
	#select brain tree difficulty
	diff = pyautogui.locateOnScreen('res/brain.png')
	pyautogui.click(diff[0]+20, diff[1])
	
	#start game (just down from difficulty button)
	pyautogui.click(diff[0]+20, diff[1]+70)
	time.sleep(2.5)
except Exception: #swallow exception. The show must go on!
	pass

sleepTime = .9
roundCount = 0
while True:
	roundCount += 1
	if roundCount == 7:
		pyautogui.typewrite('letimiyasleep')
	boxNum = 1
	analyzeBubble(727, 145, boxNum)
	boxNum = boxNum + 1 
	time.sleep(sleepTime)
	analyzeBubble(727, 66, boxNum) #box 2
	boxNum = boxNum + 1 
	time.sleep(sleepTime)
	analyzeBubble(644, 57, boxNum) #box 3
	boxNum = boxNum + 1 
	time.sleep(sleepTime)
	analyzeBubble(642, 142, boxNum) #box 4
	boxNum = boxNum + 1 
	time.sleep(sleepTime)
	analyzeBubble(590, 208, boxNum) #box 5
	boxNum = boxNum + 1 
	time.sleep(sleepTime)
	analyzeBubble(555, 133, boxNum) #box 6
	boxNum = boxNum + 1 
	time.sleep(sleepTime)
	analyzeBubble(563, 55, boxNum)  #box 7 
	boxNum = boxNum + 1 
	time.sleep(sleepTime)
	analyzeBubble(487, 88, boxNum) #box 8
	boxNum = boxNum + 1 
	time.sleep(sleepTime)
	analyzeBubble(482, 171, boxNum) #box 9
	boxNum = boxNum + 1 
	time.sleep(1)
	#click begin new round button
	pyautogui.click(487, 269) 
	time.sleep(1.75)
