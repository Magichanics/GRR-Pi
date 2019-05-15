'''
Author: Jan Garong
'''

from ControlPanelFunctions import ControlPanelFunctions
import time

def run(ip):

    cpf = ControlPanelFunctions()

    try:
        while True:

            # time this run
            start = time.time()

            # extract data
            cpf.collect_data(ip)
            cpf = ControlPanelFunctions()

            # save files
            cpf.predict_camera_data()
            cpf.get_map()

            # end timer
            print('finished iteration')
            print(time.time() - start)

    # if the user wants to exit
    except KeyboardInterrupt:
        print('finishing operations... do not forcefully exit.')

    # if file not found (means robot has not run yet)
    except FileNotFoundError:
        run(ip)

run(input('enter ip_address'))