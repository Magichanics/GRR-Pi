'''
Author: Jan Garong
Date: April 13th, 2019
'''

import math
class Mapping:

    def extend_grid(self, side, extend_by):

        # add more blank arrays at the bottom
        if side == 'south':
            for n in range(extend_by):
                self.grid.append(['w'] * len(self.grid[0]))

        # add n blank elements to the right
        if side == 'east':
            for i in range(len(self.grid)):
                for n in range(extend_by):
                    self.grid[i].append('w')

        # add blank arrays to the beginning
        if side == 'north':
            for n in range(extend_by):
                self.grid.insert(0, ['w'] * len(self.grid[0]))
            self.origin_y += extend_by

        # add n blank elements to the left
        if side == 'west':
            for i in range(len(self.grid)):
                for n in range(extend_by):
                    self.grid[i].insert(0, 'w')
            self.origin_x += extend_by

    # x and y are pure cartesian grid points
    def set_element(self, x, y, element):

        # switch signs for y values
        y = -y

        # check if exceeding south border
        if y + self.origin_y >= len(self.grid):
            self.extend_grid('south', y + self.origin_y + 1 - len(self.grid))

        # check if exceeding east border
        if x + self.origin_x >= len(self.grid[0]):
            self.extend_grid('east', x + self.origin_x + 1 - len(self.grid[0]))

        # check if exceeding north border
        if y + self.origin_y <= 0:
            self.extend_grid('north', -(y + self.origin_y))

        if x + self.origin_x <= 0:
            self.extend_grid('west', -(x + self.origin_x))

        self.grid[y + self.origin_y][x + self.origin_x] = element

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
# map_obj.create_map(3)
# map_obj.set_element(-2, -2, 'r')
# map_obj.set_element(2, 2, 'r')
# map_obj.set_element(-2, 2, 'r')
# map_obj.set_element(2, -2, 'r')
# #map_obj.set_element(20, 5, 'r')
# for i in range(len(map_obj.grid)):
#     print(map_obj.grid[i])
