'''
Author: Jan Garong & Matteo Tempo
April 20th, 2019
'''
from Mapping import Mapping
import time
import math

class BotLogger:

    def __init__(self):
        self.curr_angle = 0
        self.past_distance = 0
        self.x = 0
        self.y = 0
        self.mp = Mapping()
        self.mp.create_map(1)

    def update_coords(self, total_distance, angle, x, y): # angle is relative to the north pole

        # math.cos/sin only accepts radians
        def to_radians(input_angle):
            return (input_angle * math.pi) / 180

        # get magnitude of current vector
        magnitude = total_distance - self.past_distance

        # using SOCAHTOA get the robot location (should have decimals
        x += magnitude * math.sin(to_radians(angle))
        y += magnitude * math.cos(to_radians(angle))

        return x, y

    def forward_log(self, total_distance, angle):

        # update coordinates
        self.x, self.y = self.update_coords(total_distance, angle, self.x, self.y)

        # set total distance to be past distance
        self.past_distance = total_distance
        self.curr_angle = angle

        # set current location to R; Robot.
        self.mp.set_element(int(self.x), int(self.y), 'R')

    def block_detected(self):

        # mark the robot block 1 unit ahead as red
        red_x, red_y = self.update_coords(self.past_distance + 1, self.curr_angle,
                                          self.x, self.y)
        self.mp.set_element(int(red_x), int(red_y), 'r')

    def print_map(self, save_loc='map2d.mppy'):

        # set new robot location
        self.mp.set_element(int(self.x), int(self.y), 'R')

        # print output in textfile
        with open(save_loc, 'w') as f:
            for i in range(len(self.mp.grid)):
                output = ''
                for j in range(len(self.mp.grid[0])):
                    output += self.mp.grid[i][j]
                f.write(output + '\n')
            f.close()


