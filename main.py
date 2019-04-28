'''
placeholder console GUI
'''
from Mapping import Mapping

if __name__ == '__main__':

    map_obj = Mapping()

    try:

        # read mppy file
        file_loc = input('enter mppy file location')
        map_obj.read_mppy(file_loc)

        #
        file_loc = input('enter png file location')
        map_obj.to_img(file_loc)

    except:
        print('Error?! Terminating program.')
