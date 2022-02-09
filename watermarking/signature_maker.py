from PIL import ImageFont, ImageDraw, Image
import os

MAX_LEN = 20

def generate_signature(text, wm_filename):
    fnt="RobotoMono-Regular.ttf"
    fsize=20

    color_text="black"
    color_background="white"

    font = ImageFont.truetype(os.path.join("static", fnt), fsize)

    # In fixed-width fonts, all characters are the same size
    wint,hint = font.getsize("A")

    #image_width = wint*len(text)+2*wint
    image_width = wint*(MAX_LEN + 2) # 2 for left and right margins 
    image_heigth = 3*hint

    im = Image.new("RGB", (image_width, image_heigth), color_background)
    draw = ImageDraw.Draw(im)
    #draw.text((wint, hint), text, fill=color_text, font=font)

    hor_pos = (image_width - wint*len(text))//2
    draw.text((hor_pos, hint), text, fill=color_text, font=font)

    im.save(wm_filename)

