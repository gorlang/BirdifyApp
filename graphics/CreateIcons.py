from PIL import Image
import os

"""
Creates icon .png files of suitable size from the icon gallery file.
Img files are saved in the /output dir.
"""

def imgcrop(filepath, icon_size, x, y, w, h, n=8, m=6, offsetx=5, offsety=8):
    filename, file_extension = os.path.splitext(filepath)
    im = Image.open(filepath)
    imgwidth, imgheight = im.size
    ymargin = 3
    xmargin = 2
    for i in range(0, n):
        for j in range(0, m):
            xmargin = j + 2
            x0 = x + j * w + j * offsetx - xmargin
            y0 = y + i * h + i * offsety - ymargin
            box = (x0, y0, x0 + w + xmargin, y0 + h + ymargin)
            a = im.crop(box)
            a = a.resize((64,64), Image.ANTIALIAS)
            offset = (64 - icon_size) // 2
            box2 = (offset, offset, offset + icon_size, offset + icon_size)
            a = a.crop(box2)
            try:
                file_extension_out = ".png"
                a.save("output/" + filename + "-" + str(i) + "-" + str(j) + file_extension_out, format="png")
            except:
                pass


if __name__ == "__main__":

    icon_gallery_filename = "free-circle-icon-6-2.png"
    icon_output_size = 40
    # all input values are specific for the current icon gallery file!
    imgcrop(icon_gallery_filename, icon_output_size, 49, 40, 70, 70, n=6, m=8, offsetx=7, offsety=8)

