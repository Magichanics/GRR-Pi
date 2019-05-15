'''
GRR script; using object-oriented programming
Author: Jan Garong
'''

from BotLogger import BotLogger
from BotFunctions import BotFunctions
from multiprocessing import Process
import RPi.GPIO as GPIO
import math
import shutil
import time
import os


class GRR(BotFunctions, BotLogger):

    def take_picture(self, seconds):

        # take a picture
        self.take_img('temp/resized' + str(len(self.cl)) + '.png')

        # write robot's location, time and image location to csv sheet
        self.cl.append(str(len(self.cl)) + ',' + 'resized' + str(len(self.cl)) + '.png,' + str(self.x) + ',' +
                       str(self.y) + ',' + str(seconds) + ',' + str(self.curr_angle))


    # simplify export log method
    def export_camera_log(self, save_loc='temp/camera_log.csv'):

        with open(save_loc, 'w') as f:

            # write csv headings
            f.write(',img_name,x,y,seconds,angle\n')

            # write csv contents
            for item in self.cl:
                f.write(item + '\n')
            f.close()

    # simplify export log method into one function (merge debug and camera log functions)
    def export_debug_log(self, save_loc='temp/debug.csv'):

        with open(save_loc, 'w') as f:

            # write csv headings
            f.write(',displacement,angle,seconds\n')

            # write csv contents
            for item in self.dl:
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

        # get debug log
        self.export_debug_log(path + 'debug_log.csv')

        # zip all contents in the file
        shutil.make_archive('data', 'zip', path)

    def store_data(self):

        # get displacement
        displacement = math.sqrt(self.x ** 2 + self.y ** 2)

        # add to data
        self.dl.append(str(len(self.dl)) + ',' + str(displacement) + ','
                       + str(self.curr_angle) + ',' + str(time.time() - self.init_time))

    def log_items(self, camera_seconds, displacement_seconds):

        # check if it should take pictures
        if time.time() >= self.camera_time + camera_seconds:

            # stop the robot
            self.stop()

            # take a picture
            self.take_picture(time.time() - self.camera_time)

            # zip all data
            self.export_data_zip()

            # reset timers
            self.camera_time = time.time()
            self.velocity_time = time.time()

        # check if it should add to displacement
        if time.time() >= self.displacement_time + displacement_seconds:

            # add to data for exporting
            self.store_data()

            # reset timers
            self.displacement_time = time.time()
            self.velocity_time = time.time()

    def velocity_run(self):

        # get starting distance
        init_dist = self.dist()

        # move forward for 3 seconds
        self.forward()
        time.sleep(3)

        # get difference of distance between two points
        return abs(self.dist() - init_dist)

    def bot_run(self, camera_seconds=30, displacement_seconds=1):

        # start timer
        self.init_time = time.time()
        self.camera_time = time.time()
        self.displacement_time = time.time()
        self.store_data()

        try:

            while True:

                # check left sensors
                if GPIO.input(self.DL) == 0:
                    
                    # turn right until it detects a block
                    while GPIO.input(self.DL) == 0:
                        self.block_detected()
                        self.left()
                        self.log_items(camera_seconds, displacement_seconds)
                    self.stop()
                    self.velocity_time = time.time()
                
                # check right sensors
                if GPIO.input(self.DR) == 0:
                    
                    # turn left until it detects a block
                    while GPIO.input(self.DR) == 0:
                        self.block_detected()
                        self.right()
                        self.log_items(camera_seconds, displacement_seconds)
                    self.stop()
                    self.velocity_time = time.time()

                # move forward; calculate distance
                while GPIO.input(self.DR) and GPIO.input(self.DL):

                    # get distance/angle using ultrasonic?
                    self.curr_angle = self.get_angle()
                    self.total_distance += (self.velocity * (time.time() - self.velocity_time))/10  # vt = d
                    
                    # preform movement
                    self.forward()

                    # log forward movement
                    self.forward_log(self.total_distance, self.curr_angle)
                    
                    # get temp time
                    self.velocity_time = time.time()

                    self.log_items(camera_seconds, displacement_seconds)

                # stop robot to prevent inaccuracies
                self.stop()

        # stops when Ctrl+C
        except KeyboardInterrupt:
            
            # stop map
            GPIO.cleanup()
            
            # remove files
            self.clear_files()

    # create bot, initializing values.
    def __init__(self, velocity=36, cycle=30, frequency=300, rot_cycle=100): # velocity is 20cm/s

        # inherit functions
        BotFunctions.__init__(self, cycle=cycle, frequency=frequency)
        BotLogger.__init__(self)

        # set distances
        self.total_distance = 0
        self.curr_angle = 0
        self.velocity = velocity

        # set logs
        self.dl = []
        self.cl = []

        # call timers
        self.init_time = time.time()
        self.temp_time = time.time()
        self.camera_time = time.time()
        self.displacement_time = time.time()
        self.velocity_time = time.time()

        # create temporary directory
        if not os.path.exists('temp'):
            os.makedirs('temp')

if __name__ == '__main__':
    grr = GRR()
    #print(grr.velocity_run())
    grr.bot_run(camera_seconds=5)