'''
Author: Jan Garong
May 9th, 2019

Using the Camera manual:
https://www.waveshare.com/w/upload/6/61/RPi-Camera-User-Manual.pdf

raspistill:
https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md
'''

import PIL
from PIL import Image
import os

class CameraFunctions:

    def take_img(self, file_loc, resize=True, new_file_loc='resized.png'):
        
        print('taking picture...')
        
        # take picture using camera
        os.system('raspistill -o ' + file_loc)
        
        # resize if needed
        if resize:
            self.resize_img(file_loc, new_file_loc)

    # resize to 512x512 for neural network
    def resize_img(self, file_loc, new_file_loc):
        
        # get image
        img = Image.open(file_loc)
        
#        # determine the ratio needed to have the highest dimension down to 512
#        ratio = 512 / max(img.size[0], img.size[1])
#        
#        # resize and save image to location
#        img = img.resize((int(float(img.size[0]) * ratio), int(float(img.size[1]) * ratio)),
#                         PIL.Image.ANTIALIAS)
        
        # resize and save image to location
        img = img.resize((512, 512),
                         PIL.Image.ANTIALIAS)
        
        img.save(new_file_loc)

    def __init__(self):
        pass
    
#if __name__ == '__main__':
#    cf = CameraFunctions()
#    cf.take_img('original.png', new_file_loc='resized.png')