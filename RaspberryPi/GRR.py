'''
GRR script; using object-oriented programming
'''

import BotLogger as BotLogger
import BotFunctions as BotFunctions
import RPi.GPIO as GPIO
import time

class GRR(BotFunctions, BotLogger):

    # use angles to increment the angle away, until it reaches a difference of 90 degrees
    def rotate90(self):

        def check_angle_exceed(angle):
            if angle > 360:
                return angle - 360
            else:
                return angle

        init_angle = self.curr_angle
        while check_angle_exceed(init_angle + 90) < self.curr_angle:
            self.curr_angle = ???
            Ab.left()
            time.sleep(0.01)
        Ab.stop()
        time.sleep(0.5)

    def bot_run(self):

        try:

            while True:

                # check sensors
                DR_status = GPIO.input(self.DR)
                DL_status = GPIO.input(self.DL)

                # if it hits object using infrared
                if DL_status == 0 or DR_status == 0:
                    rotate90()
                    self.block_detected(self.total_distance)
                    direction = rotate90_dict[direction]  # new direction
                    print(direction)

                # move forward; calculate distance
                else:

                    self.forward()
                    # get distance/angle using ultrasonic
                    self.total_distance = ???
                    self.curr_angle = ???
                    self.total_distance += distance
                    self.forward_log(self.total_distance, self.curr_angle)

        # stops when Ctrl+C
        except KeyboardInterrupt:
            self.print_map()
            GPIO.cleanup();

    # create bot
    def __init__(self):
        BotFunctions.__init__(cycle=10, frequency=100)
        BotLogger.__init__()
        self.total_distance = 0

