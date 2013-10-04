#!/usr/bin/env
# Removes the shadow from MacOS-Generated screen shots.

import Image,os

if __name__=="__main__":
    image = Image.open(os.sys.argv[1])
    image = image.convert('RGBA')

    (width,height) = image.size
    def find_first_non_alpha_x():
        for i in range(width):
            if image.getpixel((i,height/2))[3]==255:
                return i
        raise RuntimeError("No non-alpha pixels on midline")

    def find_last_non_alpha_x():
        for i in range(width-1,0,-1):
            if image.getpixel((i,height/2))[3]==255:
                return i
        raise RuntimeError("No non-alpha pixels on midline")

    def find_first_non_alpha_y():
        for i in range(height):
            if image.getpixel((width/2,i))[3]==255:
                return i
        raise RuntimeError("No non-alpha pixels on midline")

    def find_last_non_alpha_y():
        for i in range(height-1,0,-1):
            if image.getpixel((width/2,i))[3]==255:
                return i
        raise RuntimeError("No non-alpha pixels on midline")

    x1 = find_first_non_alpha_x()
    y1 = find_first_non_alpha_y()
    x2  = find_last_non_alpha_x()
    y2  = find_last_non_alpha_y()
    
    y = image.crop((x1-1,y1-1,x2+1,y2+1))
    y.save(os.sys.argv[1]+"-cropped.png")

