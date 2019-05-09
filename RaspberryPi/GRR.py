'''
GRR script; using object-oriented programming
Author: Jan Garong
'''

from BotLogger import BotLogger
from BotFunctions import BotFunctions
from CameraFunctions import CameraFunctions
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
    
    def velocity_run(self):
        
        # get starting distance
        init_dist = self.dist()
        
        # move forward for 3 seconds
        self.forward()
        time.sleep(3)
        
        # get difference of distance between two points
        return abs(self.dist() - init_dist)

    def bot_run(self):

        try:

            while True:

                # check left sensors
                if GPIO.input(self.DL) == 0:
                    
                    # turn right until it detects a block
                    while GPIO.input(self.DL) == 0:
                        self.block_detected()
                        self.left()
                    self.stop()
                    self.temp_time = time.time()
                
                # check right sensors
                if GPIO.input(self.DR) == 0:
                    
                    # turn left until it detects a block
                    while GPIO.input(self.DR) == 0:
                        self.block_detected()
                        self.right()
                    self.stop()
                    self.temp_time = time.time()

                # move forward; calculate distance
                #else:
                while (GPIO.input(self.DR) and GPIO.input(self.DL)):
                    
                    #print(self.dist())

                    # get distance/angle using ultrasonic?
                    self.curr_angle = self.get_angle()
                    self.total_distance += (self.velocity * (time.time() - self.temp_time))/10 # vt = d
                    self.debug_log()
                    
                    # preform movement
                    self.forward()

                    # log forward movement
                    self.forward_log(self.total_distance, self.curr_angle)
                    
                    # get temp time
                    self.temp_time = time.time()
                    
                # stop robot to prevent inaccuracies
                self.stop()
                
                self.print_map()

        # stops when Ctrl+C
        except KeyboardInterrupt:
            
            # stop map
            GPIO.cleanup()
            
            # save items
            self.print_map()
            if self.debug_mode:
                self.export_debug_log()
                
            # take a picture
            cf = CameraFunctions()
            cf.take_img('original.png', new_file_loc='resized.png')

    # create bot, initializing values.
    def __init__(self, debug_mode=False, velocity=36, cycle=30, frequency=300, rot_cycle=100): # velocity is 20cm/s
        self.debug_mode = debug_mode
        self.velocity = velocity
        BotFunctions.__init__(self, cycle=cycle, frequency=frequency)
        BotLogger.__init__(self)
        self.total_distance = 0
        self.dl = []
        self.init_time = time.time()
        self.temp_time = self.init_time

if __name__ == '__main__':
    grr = GRR()
    #print(grr.velocity_run())
    grr.bot_run()