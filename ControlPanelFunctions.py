'''
Author: Jan Garong
May 5th, 2019
'''
from Mapping import Mapping
import os

class ControlPanelFunctions:

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

    def __init__(self):
        pass

if __name__ == '__main__':

    cpf = ControlPanelFunctions()

    ip = input('enter ip address')

    # get user input
    cpf.read_from_pi(ip, '~/map2d.mppy', '.')
    loc2 = input('enter png file location')

    # export to image
    cpf.mppy_to_img('map2d.mppy', loc2)
