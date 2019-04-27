'''
Author: Matteo Tempo
Date: April 22nd, 2019
'''

from PyQt5 import QtWidgets, QtGui, uic
from ImageProcess import ImageProcess
from Mapping import Mapping

import sys

# makes app and loads window config file
app = QtWidgets.QApplication([])
win = uic.loadUi("GUI.ui")  # specify the location of your .ui file

# export and display method
def export():
    # make map object
    map_obj = Mapping()
    map_obj.create_map(3)
    map_obj.set_element(-2, -2, 'r')
    map_obj.set_element(2, 2, 'r')
    map_obj.set_element(-2, 2, 'r')
    map_obj.set_element(9, -2, 'g')

    # display map object onto label
    ImageProcess.make_grid_image(win, map_obj)
    win.gridImage.setPixmap(QtGui.QPixmap('rectangle.png'))


# assign event listener to export function
win.btnExport.clicked.connect(export)

# show window
win.show()

# on exit window, close
sys.exit(app.exec())
