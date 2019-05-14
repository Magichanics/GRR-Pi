'''
Author: Jan Garong
'''

import cv2
from ControlPanelFunctions import ControlPanelFunctions

ip = input('enter ip_address')

cpf = ControlPanelFunctions()

# extract data
cpf.collect_data(ip)

# # export to image
# cpf.mppy_to_img('temp/mp2d.png')
#
# # resize image
# img_display = cv2.imread('temp/original.png')
# img_display.resize((512,512))
#
# # predict image
# img_array = cpf.img_to_array('temp/original.png')
# y_test = cpf.nn.predict(img_array,
#                         confidence_threshold=0.65)
# print(y_test)
# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow('image',img_display)
# cv2.waitKey(0)
# cv2.destroyAllWindows()