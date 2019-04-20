'''
Based off of Infrared_Obstacle_Avoidance.py by waveshare
'''
import RPi.GPIO as GPIO
import time
from BotLogger import BotLogger
from AlphaBot2 import AlphaBot2

class GreatRoamingRobot:

    # rotate 90 degrees
    def rotate90(self):
        self.Ab.left()
        time.sleep(0.15)
        self.Ab.stop()
        time.sleep(0.5)

    # starts and stop for t seconds
    def timed_start(self, seconds):
        try:
            self.Ab.forward()
            time.sleep(seconds)
            GPIO.cleanup()
        except KeyboardInterrupt:
            GPIO.cleanup();

    def start(self):

        # initialize dictionary (for left 90 degree rotations)
        rotate90_dict = {'north': 'west',
                         'west': 'south',
                         'south': 'east',
                         'east': 'north'}

        try:
            while True:

                direction = 'north' # or forward, north is relative in this case.

                # track time
                t1 = time.time()

                # check sensors
                DR_status = GPIO.input(self.DR)
                DL_status = GPIO.input(self.DL)

                # if it hits object using infrared
                if((DL_status == 0) or (DR_status == 0)):
                    self.rotate90()
                    self.blog.block_detected(direction)
                    direction = rotate90_dict[direction] # new direction

                # move forward; calculate distance
                else:
                    self.Ab.forward()

                    # get end time and distance
                    t2 = time.time()
                    distance = (t2 - t1) * self.velocity

                    # trace coordinates
                    self.blog.add_distance(distance, direction)

        # stops when Ctrl+C
        except KeyboardInterrupt:
            blog.print_map()
            GPIO.cleanup();
        
    # set IDs for the given robot
    def __init__(self, velocity=10,
                 cycle=10, frequency=100): # velocity is precalculuated

        self.blog = BotLogger()
        self.velocity = velocity
        self.Ab = AlphaBot2(cycle=cycle, frequency=frequency) # 10cm/s
        self.DR = 16
        self.DL = 19
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.DR,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.DL,GPIO.IN,GPIO.PUD_UP)


