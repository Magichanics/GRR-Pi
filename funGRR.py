'''
GRR script; using functional programming

'''
import RPi.GPIO as GPIO
import time
from BotLogger import BotLogger
from AlphaBot2 import AlphaBot2

Ab = AlphaBot2(cycle=10, frequency=100)
blog = BotLogger()
velocity = 10 # in cm/s
DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

# rotate 90 degrees
def rotate90():
    Ab.left()
    time.sleep(0.15)
    Ab.stop()
    time.sleep(0.5)
    
# initialize dictionary (for left 90 degree rotations)
rotate90_dict = {'north': 'west',
                 'west': 'south',
                 'south': 'east',
                 'east': 'north'}

direction = 'north' # or forward, north is relative in this case.

try:
    
    while True:

        # track time
        t1 = time.time()

        # check sensors
        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)

        # if it hits object using infrared
        if((DL_status == 0) or (DR_status == 0)):
            rotate90()
            blog.block_detected(direction)
            direction = rotate90_dict[direction] # new direction
            print(direction)

        # move forward; calculate distance
        else:
            Ab.forward()

            # get end time and distance
            t2 = time.time()
            distance = (t2 - t1) * velocity

            # trace coordinates
            #print(self.blog.coords)
            blog.add_distance(distance, direction)
        
# stops when Ctrl+C
except KeyboardInterrupt:
    blog.print_map()
    GPIO.cleanup();

