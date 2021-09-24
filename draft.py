from PIL import Image, ImageDraw, ImageFont

image = Image.new("RGB", (200, 100))
font_filepath = "example_data/font/simsun.ttf"
font_size = 50

draw = ImageDraw.Draw(image)
font = ImageFont.truetype(font_filepath, font_size)

xy = (40, 20)
text = "hello"

draw.text(xy, text, font=font)
import ipdb; ipdb.set_trace(context=10)
for i, char in enumerate(text):
	right, bottom = font.getsize(text[:i+1])
	width, height = font.getmask(char).size
	right += xy[0]
	bottom += xy[1]
	top = bottom - height
	left = right - width
	
	draw.rectangle((left, top, right, bottom), None, "#f00")

image.show()
