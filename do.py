import os
from posixpath import basename
import re
import sys
from PIL import Image,ImageDraw,ImageFont
import glob
image_list = []
for filename in glob.glob('sourceImages/*.png'): 
    im=Image.open(filename)
    image_list.append({
        "image":im,
        "path":filename
    })
    for c in range(filename.count("²")):
        image_list.append(
            "filler"
        )
    

def drawText(im :Image,text):
    
    box = ((0, 0, im.width, im.height*0.8))
    draw = ImageDraw.Draw(im)
    
    font_size = 600
    size = None
    while (size is None or size[2] > box[2] - box[0] or size[3] > box[3] - box[1]) and font_size > 0:
        font = ImageFont.truetype("Comic.ttf", font_size)
        size = draw.multiline_textbbox((box[0],box[1]), text, font=font, anchor=None, spacing=4, align='left', direction=None, features=None, language=None, stroke_width=0, embedded_color=False)
        font_size -= 1
    
    draw.multiline_text((box[0], box[1]), text, "#FFFFFF", font,stroke_fill="#000",stroke_width=5)
    return im

for i,image in enumerate(image_list):
    print("Processing image",image)
    if(image=="filler"):
        continue
    angle = 360*i/len(image_list)
    textPrint = os.path.basename(image["path"]).replace(".png","").replace("²","").strip()
    
    textPrint=textPrint.split(" ")[1:]
    textPrint = "\n".join(textPrint).strip()
    image["image"].thumbnail([sys.maxsize, 500], Image.Resampling.LANCZOS)    
    # image["image"]=  image["image"].resize((300, 300))
    image["image"]= drawText( image["image"],textPrint)
    image["image"]= image["image"].rotate(angle,expand=1)

for filename in glob.glob('destImages/*.png'): 
    os.unlink(filename)
for i,image in enumerate(image_list):
        if(image=="filler"):
            continue
        id = str(len(image_list)-i).zfill(5)
        image["image"].save(f"destImages/image-{id}.png") 
        