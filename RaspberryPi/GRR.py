'''
GRR script; using object-oriented programming
Author: Jan Garong
'''

from BotLogger import BotLogger
from BotFunctions import BotFunctions
import RPi.GPIO as GPIO
import time

class GRR(BotFunctions, BotLogger):
    
    # use angles to increment the angle away, until it reaches a difference of 90 degrees
    def rotate90(self):

        def check_angle_exceed(angle):
            if angle < 0:
                return angle + 360
            else:
                return angle
            
        def rotate90_condition(angle1, angle2):
            if past360: #angle1 > angle2 initially
                return angle1 > angle2
            else:
                return angle1 < angle2

        init_angle = self.curr_angle
        
        # check whether it is past 360 or not
        if check_angle_exceed(init_angle - 90) < init_angle:
            past360 = False
        else:
            past360 = True
        
        # turn left until it is roughly 90 degrees left.
        while rotate90_condition(check_angle_exceed(init_angle - 90),
                                 self.curr_angle):
            self.curr_angle = self.get_angle()
            self.left()
        self.stop()
        time.sleep(0.5)
        
    def rotate90_timed(self):
        self.left()
        time.sleep(0.15)
        self.stop()
        time.sleep(0.5)

    def bot_run(self):

        try:

            while True:

                # check sensors
                DR_status = GPIO.input(self.DR)
                DL_status = GPIO.input(self.DL)

                # if it hits object using infrared
                if DL_status == 0 or DR_status == 0:
                    self.rotate90_timed()
                    self.block_detected()
                    #time.sleep(0.5)
                    #direction = rotate90_dict[direction]  # new direction
                    #print(direction)

                # move forward; calculate distance
                else:

                    self.forward()
                    # get distance/angle using ultrasonic?
                    self.curr_angle = self.get_angle()
                    self.total_distance += 0.01
                    self.forward_log(self.total_distance, self.curr_angle)

        # stops when Ctrl+C
        except KeyboardInterrupt:
            self.print_map()
            GPIO.cleanup();

    # create bot
    def __init__(self):
        BotFunctions.__init__(self)
        BotLogger.__init__(self)
        self.total_distance = 0

if __name__ == '__main__':
    grr = GRR()
    grr.bot_run()