# import PIL
from PIL import Image, ImageDraw
import numpy as np


class WaterMark:
    SUCCESS = 1
    FAILURE = -1

    def __init__(self, file_name, leaf_file_name=r'leaf.png'):
        self._file_name = file_name
        self._leaf_file_name = leaf_file_name

    def addWaterMark(self, new_width=400):
        file = Image.open(self._file_name)
        leaf_file = Image.open(self._leaf_file_name)
        if file.mode == 'RGB':
            file.putalpha(255)
        elif file.mode != 'RGBA':
            return WaterMark.FAILURE, file

        width, height = file.size
        ratio = new_width / width
        new_h = int(ratio * height)
        file = file.resize((new_width, new_h),
                           Image.Resampling.LANCZOS)
        im = Image.new(mode='RGBA', size=(new_width, new_h), color=0)
        im.paste(file)
        im.paste(im=leaf_file, box=None, mask=leaf_file)
        file.close()
        leaf_file.close()
        path = 'hi.png'
        im.save(path)
        return WaterMark.SUCCESS, path


if __name__ == '__main__':
    pass
# a = WaterMark(r'3.jpg')
# ret, im = a.addWaterMark()
