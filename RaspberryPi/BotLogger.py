'''
Author: Jan Garong
April 20th, 2019
'''
from Mapping import Mapping
import time

class BotLogger:

    def block_detected(self, direction):

        # mark the robot block ahead as red
        if direction == 'north':
            self.mp.set_element(int(self.coords[0]), int(self.coords[1]) + 1, 'r')

        elif direction == 'south':
            self.mp.set_element(int(self.coords[0]), int(self.coords[1]) - 1, 'r')

        elif direction == 'east':
            self.mp.set_element(int(self.coords[0]) + 1, int(self.coords[1]), 'r')

        elif direction == 'west':
            self.mp.set_element(int(self.coords[0]) - 1, int(self.coords[1]), 'r')

    # distance is in cm
    def add_distance(self, distance, direction):

        if direction == 'north':

            # add to y coord; moves up.
            self.coords[1] += distance

            # set new robot location
            self.mp.set_element(int(self.coords[0]), int(self.coords[1]), 'R')

            # set previous block to green; passable area
            self.mp.set_element(int(self.coords[0]), int(self.coords[1]) - 1, 'g')

        elif direction == 'south':
            self.coords[1] -= distance
            self.mp.set_element(int(self.coords[0]), int(self.coords[1]), 'R')
            self.mp.set_element(int(self.coords[0]), int(self.coords[1]) + 1, 'g')

        elif direction == 'east':
            self.coords[0] += distance
            self.mp.set_element(int(self.coords[0]), int(self.coords[1]), 'R')
            self.mp.set_element(int(self.coords[0]) - 1, int(self.coords[1]), 'g')

        elif direction == 'west':
            self.coords[0] -= distance
            self.mp.set_element(int(self.coords[0]), int(self.coords[1]), 'R')
            self.mp.set_element(int(self.coords[0]) + 1, int(self.coords[1]), 'g')

    def print_map(self, save_loc='map2d.mppy'):

        # print output in textfile
        with open(save_loc, 'w') as f:
            for i in range(len(self.mp.grid)):
                output = ''
                for j in range(len(self.mp.grid[0])):
                    output += self.mp.grid[i][j]
                f.write(output + '\n')
            f.close()


    def __init__(self):
        self.coords = [0, 0]
        self.mp = Mapping()
        self.mp.create_map(1)

# blog = BotLogger()
# blog.add_distance(1, 'north')
# blog.block_detected('north')
# blog.add_distance(1, 'west')
# blog.block_detected('west')
# blog.add_distance(1, 'south')
# blog.block_detected('south')
# blog.add_distance(1, 'east')
# blog.print_map()