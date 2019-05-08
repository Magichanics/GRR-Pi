'''
GRR script; using object-oriented programming
Author: Jan Garong
'''

from BotLogger import BotLogger
from BotFunctions import BotFunctions
import RPi.GPIO as GPIO
import time

class GRR(BotFunctions, BotLogger):

    # get the current angle and total distance, and add to list
    def debug_log(self):
        if self.debug_mode:
            self.dl.append(str(len(self.dl) - 1) + ',' + str(self.total_distance) + ',' \
                           + str(self.curr_angle) + ',' + str(time.time() - self.init_time))
        else:
            pass
        
    # save log to text
    def export_debug_log(self, save_loc='debug_logs.txt'):
        if self.debug_mode:
            with open(save_loc, 'w') as f:

                # write csv headings
                f.write(',total_distance,angle,seconds')

                # write csv contents
                for item in self.dl:
                    f.write(item + '\n')
                f.close()
        else:
            pass

    def bot_run(self):

        try:

            while True:

                # check left sensors
                if GPIO.input(self.DL) == 0: # simplify
                    
                    # turn right until it detects a block
                    while GPIO.input(self.DL) == 0:
                        self.block_detected()
                        self.left()
                    self.stop()
                
                # check right sensors
                if GPIO.input(self.DR) == 0:
                    
                    # turn left until it detects a block
                    while GPIO.input(self.DR) == 0:
                        self.block_detected()
                        self.right()
                    self.stop()

                # move forward; calculate distance
                #else:
                while (GPIO.input(self.DR) and GPIO.input(self.DL)):

                    # get distance/angle using ultrasonic?
                    self.curr_angle = self.get_angle()
                    self.total_distance += 0.02
                    self.debug_log()
                    
                    # preform movement
                    self.forward()

                    # log forward movement
                    self.forward_log(self.total_distance, self.curr_angle)
                    
                # stop robot to prevent inaccuracies
                self.stop()
                
                self.print_map()

        # stops when Ctrl+C
        except KeyboardInterrupt:
            self.print_map()
            self.export_debug_log()
            GPIO.cleanup()

    # create bot
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        BotFunctions.__init__(self, cycle=20, frequency=200)
        BotLogger.__init__(self)
        self.total_distance = 0
        self.dl = []
        self.init_time = time.time()

if __name__ == '__main__':
    grr = GRR()
    grr.bot_run()