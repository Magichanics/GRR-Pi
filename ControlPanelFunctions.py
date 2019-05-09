'''
Author: Jan Garong
May 5th, 2019
'''
from Mapping import Mapping
from imageio import imread
from keras.preprocessing import image
from SSDKeras import SDDNeuralNetwork512
import os

class ControlPanelFunctions:

    def img_to_array(self, img_path):
        # convert image to array to fit into neural network
        img = image.load_img(img_path, target_size=(512, 512))
        img = image.img_to_array(img)
        return img

    def read_from_pi(self, ip_address, pi_file_loc,
                     save_loc):

        # read from pi robot using commandline and scp
        os.system('scp pi@' + ip_address + ':' + pi_file_loc + ' '
                  + save_loc)

    def mppy_to_img(self, mppy_loc, img_loc):

        # read mppy file
        map_obj = Mapping()
        map_obj.read_mppy(mppy_loc)

        # export to png
        map_obj.to_img(img_loc)

    # initialize neural network
    def __init__(self):
        self.nn = SDDNeuralNetwork512(weights_path='VGG_VOC0712_SSD_512x512_iter_120000.h5')


