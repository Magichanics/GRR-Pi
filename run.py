'''
Author: Jan Garong
'''

from ControlPanelFunctions import ControlPanelFunctions
import time

ip = input('enter ip_address')

cpf = ControlPanelFunctions()

try:
    while True:

        # extract data
        cpf.collect_data(ip)
        cpf = ControlPanelFunctions()

        # save files
        cpf.predict_camera_data()
        cpf.get_map()

        # 1 second delay
        time.sleep(1)

except KeyboardInterrupt:
    print('finishing operations...')