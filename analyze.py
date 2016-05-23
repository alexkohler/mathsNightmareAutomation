from PIL import Image
import sys
import pytesseract

img = Image.open('lol.png')
img = img.convert("RGBA")

pixdata = img.load()

# Clean the background noise, if color != white, then set to black.

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        #print(pixdata[x, y])
        if pixdata[x, y][1] > 90: #| pixdata[x,y][0] == 117:
            pixdata[x, y] = (255, 255, 255, 255)
        if pixdata[x, y][0] == 117: #| pixdata[x,y][0] == 117:
            pixdata[x, y] = (255, 255, 255, 255)
        #print(pixdata[x,y][2])
        #if pixdata[x,y][2] != 137:

#Jfor y in xrange(img.size[1]):
    #for x in xrange(img.size[0]):
        #print(pixdata[x, y])
        #if pixdata[x, y][1] > 90:
            #pixdata[x, y] = (255, 255, 255, 255)

num1=pytesseract.image_to_string(img, config='-psm 8 digits').replace(" ", "").replace("-", "").replace(".", "")
print(num1)
img.show()
