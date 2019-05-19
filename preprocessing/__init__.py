'''
Author: Jan Garong
'''

from preprocessing.CPFunctions import CPFunctions

def fetch_assets(ip):
    cpf = CPFunctions()

    # extract data
    cpf.collect_data(ip)

    # save files
    cpf.predict_camera_data()
    cpf.get_map()
    cpf.graph_items()

