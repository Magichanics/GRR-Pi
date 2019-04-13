'''
Author: Jan Garong
Date: April 13th, 2019
'''
import math
class Mapping:

    def create_map(self, init_size=15):

        # check if its odd
        if init_size % 2 == 0:
            print('Size must be odd.')
            return

        # create 2d array
        self.grid = [['w'] * init_size for _ in range(init_size)]

        # determine centerpoint (0,0)
        self.origin_x = math.floor(len(self.grid) / 2)
        self.origin_y = math.floor(len(self.grid) / 2)

        # set robot's location at origin
        self.grid[self.origin_y][self.origin_x] = 'R'

    def __init__(self):
        pass

# map_obj = Mapping()
# map_obj.create_map()
# for i in range(len(map_obj.grid)):
#     print(map_obj.grid[i])
