'''
Author: Jan Garong
May 5th, 2019
'''
from Mapping import Mapping
from keras.preprocessing import image
from SSDKeras import SDDNeuralNetwork512
import os
import zipfile

class ControlPanelFunctions:

    def img_to_array(self, img_path):
        # convert image to array to fit into neural network
        img = image.load_img(img_path, target_size=(512, 512))
        img = image.img_to_array(img)
        return img

    def collect_data(self, ip_address, data_path='~/data.zip',
                     save_path='temp/'):

        # read from pi robot using commandline and scp
        os.system('scp pi@' + ip_address + ':' + data_path + ' '
                  + save_path)

        # unzip
        zr = zipfile.Zipfile('temp/data.zip','r')
        zr.extractall('temp/')
        zr.close()

        # delete file

    # def mppy_to_img(self, img_map_loc):
    #
    #     # read mppy file
    #     map_obj = Mapping()
    #     map_obj.read_mppy(self.mppy_loc)
    #
    #     # export to png
    #     map_obj.to_img(img_map_loc)

    # initialize neural network
    def __init__(self):

        # assign weights and neural network
        self.nn = SDDNeuralNetwork512(weights_path='VGG_VOC0712_SSD_512x512_iter_120000.h5')

        # create temporary directory
        if not os.path.exists('temp'):
            os.makedirs('temp')


