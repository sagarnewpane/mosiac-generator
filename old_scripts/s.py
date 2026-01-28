from PIL import Image,ImageDraw,ImageFont
import math

# bg = Image.new('RGB', (300,600), color = (0, 0, 0))
# oneCharWidth , oneCharHeight = 20,20
# img = Image.open('1.jpg')

def changeColor(orginal_img,r,g,b):
	colr = (r,g,b)
	w,h = orginal_img.size
	bg = Image.new('RGBA', (w,h), color = colr)
	bg.putalpha(100)
	orginal_img.paste(bg,(0,0),bg)
	return orginal_img
			
# imr = im.resize((20,20))
# changeColor(img)
# bg.show()
