'''
Based off of Infrared_Obstacle_Avoidance.py
'''
import RPi.GPIO as GPIO
import time
from AlphaBot2 import AlphaBot2

Ab = AlphaBot2()

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

try:
    while True:
        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)
        if((DL_status == 0) or (DR_status == 0)):

            # move 90 degrees left
            Ab.left()
            time.sleep(0.15)

            # stop so the sensors will not trigger again
            Ab.stop()
            time.sleep(0.5)

        else:

            # move forward
            Ab.forward()

except KeyboardInterrupt:
    GPIO.cleanup();

