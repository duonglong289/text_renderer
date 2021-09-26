from PIL import Image, ImageDraw, ImageFont

image = Image.new("RGB", (1000, 100))
font_filepath = "example_data/font/simsun.ttf"
font_size = 50

draw = ImageDraw.Draw(image)
font = ImageFont.truetype(font_filepath, font_size)

xy = (40, 20)
text = "hello mudakfakagg"

for i, char in enumerate(text):
    right, bottom = font.getsize(text[:i+1])
    width, height = font.getmask(char).size

    top = font.getoffset(char)[1]
    bottom = font.getsize(char)[1]
    left = right - width

    draw.rectangle((left, top, right, bottom), None, "#f00")

    top -= font.getoffset(char)[1]
    print(font.getoffset(char)[1])
    draw.text((left, top), text[i], font=font)

image.show()
