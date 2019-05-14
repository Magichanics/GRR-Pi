'''
GRR script; using object-oriented programming
Author: Jan Garong
'''

from BotLogger import BotLogger
from BotFunctions import BotFunctions
from multiprocessing import Process
import RPi.GPIO as GPIO
import shutil
import time
import os


class GRR(BotFunctions, BotLogger):

    def take_picture(self):

        # take a picture
#        p = Process(target=self.take_img,
#                    args=('resized' + str(len(self.cl)) + '.png'))
#
#
#        # start separate process
#        p.start()
#        p.join()
        
        self.take_img('temp/resized' + str(len(self.cl)) + '.png')

        # write robot's location and image location to csv sheet
        self.cl.append(str(len(self.cl)) + ',' + 'resized' + str(len(self.cl)) + '.png,' + str(self.x) + ',' +
                       str(self.y))

    # get the current angle and total distance, and add to list
    def debug_log(self):
        if self.debug_mode:
            self.dl.append(str(len(self.dl)) + ',' + str(self.total_distance) + ',' \
                           + str(self.curr_angle) + ',' + str(time.time() - self.init_time) \
                           + ',' + str(self.dist()))
        else:
            pass
        
    # save log to text
    def export_debug_log(self, save_loc='debug_logs.csv'):
        with open(save_loc, 'w') as f:

            # write csv headings
            f.write(',total_distance,angle,seconds,ultrasonic_distance\n')

            # write csv contents
            for item in self.dl:
                f.write(item + '\n')
            f.close()

    def export_camera_log(self, save_loc='temp/camera_log.csv'):
        with open(save_loc, 'w') as f:

            # write csv headings
            f.write(',img_name,x,y\n')

            # write csv contents
            for item in self.cl:
                f.write(item + '\n')
            f.close()
            
    def clear_files(self, path='temp/'):
        
        # unlink files in folder
        for file in os.listdir(path):
            file_path = os.path.join(path, file) # get file path

            # remove file
            if os.path.isfile(file_path):
                os.unlink(file_path)

            # remove directory
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        

    def export_data_zip(self, path='temp/'):

        # get map
        self.print_map(path + 'map.txt')

        # get camera log
        self.export_camera_log(path + 'camera_log.csv')

        # zip all contents in the file
        shutil.make_archive('data', 'zip', path)


    def velocity_run(self):
        
        # get starting distance
        init_dist = self.dist()
        
        # move forward for 3 seconds
        self.forward()
        time.sleep(3)
        
        # get difference of distance between two points
        return abs(self.dist() - init_dist)

    def bot_run(self, camera_timer=30):

        # start timer
        self.start_time = time.time()

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

                    # check if it's time to take a picture in 10 seconds
                    if self.start_time + camera_timer <= time.time():
                        self.stop()
                        self.take_picture()
                        self.export_data_zip()
                        self.start_time = time.time()
                        self.temp_time = time.time()


                # stop robot to prevent inaccuracies
                self.stop()

        # stops when Ctrl+C
        except KeyboardInterrupt:
            
            # stop map
            GPIO.cleanup()
            
            # remove files
            self.clear_files()
            if self.debug_mode:
                self.export_debug_log()


    # create bot, initializing values.
    def __init__(self, debug_mode=False, velocity=36, cycle=30, frequency=300, rot_cycle=100): # velocity is 20cm/s
        self.debug_mode = debug_mode
        self.velocity = velocity
        BotFunctions.__init__(self, cycle=cycle, frequency=frequency)
        BotLogger.__init__(self)
        self.total_distance = 0
        self.dl = [] # debug log
        self.cl = [] # camera log
        self.init_time = time.time()
        self.temp_time = self.init_time

        # create temporary directory
        if not os.path.exists('temp'):
           os.makedirs('temp')

        # # create blank files for modification
        # open("temp/map.txt","w+").close()
        # open('temp/debug_logs.csv',"w+").close()


if __name__ == '__main__':
    grr = GRR()
    #print(grr.velocity_run())
    grr.bot_run(camera_timer=5)