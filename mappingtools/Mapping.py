'''
Author: Matteo Tempo, Jan Garong
Date: April 13th, 2019
'''

import math
from PIL import Image
from PIL import ImageDraw


class Mapping:

    # gets coordinate value
    def get_coords(self, x, y):
        return self.grid[-y + self.origin_y][self.origin_x + x]

    def get_index(self, p):
        return -p[1] + self.origin_y, self.origin_x + p[0]

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

    def check_element(self, x, y):

        try:
            return self.grid[self.origin_y - y][x + self.origin_x]

        # if out of bounds
        except IndexError:
            return 'w'

    # x and y are pure cartesian grid points
    def set_element(self, x, y, element):

        # switch signs for y values
        y = -y

        # uses a list of if statements since x and y coordinates could be diagonal
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
        self.origin_x = int(math.floor(len(self.grid) / 2))
        self.origin_y = int(math.floor(len(self.grid) / 2))

        # set robot's location at origin
        self.grid[self.origin_y][self.origin_x] = 'R'

    def read_mppy(self, file_loc):

        temp_grid = []

        # open file location
        with open(file_loc, 'r') as f:

            # get first line
            line = f.readline()
            y = 0
            while line != '':

                # clean string from \ns
                line = line.strip()

                # append each character
                row = []
                for i in range(len(line)):
                    row.append(line[i])

                    # look for origin
                    if line[i] == 'y':
                        self.origin_x = i
                        self.origin_y = y

                temp_grid.append(row)

                # get next line
                line = f.readline()
                y += 1

        f.close()

        self.grid = temp_grid

    def to_img(self, file_loc='map.png'):

        # create color dictionary
        char_dict = {"R": "black",
                     "r": "red",
                     "g": "green",
                     "w": "white",
                     "y": "yellow",
                     "o": "orange"}

        x = len(self.grid[0])
        y = len(self.grid)

        # create new rgb image
        img = Image.new('RGB', (x * 50, y * 50), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        fill_colour = ""
        for col in range(y):
            for row in range(x):

                # draw square based on color
                fill_colour = char_dict[self.grid[col][row]]
                draw.rectangle([(row * 50, col * 50), (row * 50 + 49, col * 50 + 49)], fill=fill_colour,
                               outline="black")

        img.save(file_loc)

    def __init__(self):
        pass