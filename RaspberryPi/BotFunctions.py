'''
Original code from waveshare (AlphaBot2.py)

Find Heading by using HMC5883L interface with Raspberry Pi using Python
http://www.electronicwings.com

'''
import RPi.GPIO as GPIO
import time
import smbus        #import SMBus module of I2C
#from time import sleep  #import sleep
import math

class BotFunctions:

    # if the user wants to change the speed.
    def stop_set_speed(self, cycle, frequency):

        self.PA = cycle
        self.PB = cycle
        self.PWMA = GPIO.PWM(self.ENA, frequency) # left and right motor
        self.PWMB = GPIO.PWM(self.ENB, frequency)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def __init__(self, ain1=12, ain2=13, ena=6,
                 bin1=20, bin2=21, enb=26, cycle=20, dr=16, dl=19,
                 frequency=200):

        # set socket ids
        # movement
        self.AIN1 = ain1
        self.AIN2 = ain2
        self.BIN1 = bin1
        self.BIN2 = bin2
        self.ENA = ena # left motor
        self.ENB = enb # right motor

        # infrared sensors
        self.DR = dr
        self.DL = dl

        # no. of cycles
        self.PA = cycle
        self.PB = cycle

        # use hardware with the code
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # motors (etc.)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)

        # sensors
        GPIO.setup(self.DR, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.DL, GPIO.IN, GPIO.PUD_UP)
        self.stop_set_speed(cycle, frequency)

        # compass code

        # some MPU6050 Registers and their Address
        self.Register_A = 0  # Address of Configuration register A
        self.Register_B = 0x01  # Address of configuration register B
        self.Register_mode = 0x02  # Address of mode register

        self.X_axis_H = 0x03  # Address of X-axis MSB data register
        self.Z_axis_H = 0x05  # Address of Z-axis MSB data register
        self.Y_axis_H = 0x07  # Address of Y-axis MSB data register
        self.declination = -0.00669  # define declination angle of location where measurement going to be done

        self.bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
        self.Device_Address = 0x1e  # HMC5883L magnetometer device address

        self.Magnetometer_Init()  # initialize HMC5883L magnetometer

    def get_angle(self):

        # Read Accelerometer raw value
        x = self.read_raw_data(self.X_axis_H)
        z = self.read_raw_data(self.Z_axis_H)
        y = self.read_raw_data(self.Y_axis_H)

        heading = math.atan2(y, x) + self.declination

        # Due to declination check for >360 degree
        if (heading > 2 * math.pi):
            heading = heading - 2 * math.pi

        # check for sign
        if (heading < 0):
            heading = heading + 2 * math.pi

        # convert into angle
        heading_angle = int(heading * 180 / math.pi)

        return heading_angle

    def Magnetometer_Init(self):
        # write to Configuration Register A
        self.bus.write_byte_data(self.Device_Address, self.Register_A, 0x70)

        # Write to Configuration Register B for gain
        self.bus.write_byte_data(self.Device_Address, self.Register_B, 0xa0)

        # Write to mode Register for selecting mode
        self.bus.write_byte_data(self.Device_Address, self.Register_mode, 0)

    def read_raw_data(self, addr):

        # Read raw 16-bit value
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr + 1)

        # concatenate higher and lower value
        value = ((high << 8) | low)

        # to get signed value from module
        if (value > 32768):
            value = value - 65536
        return value

    def forward(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.HIGH)


    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)

    def backward(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.LOW)

    def left(self):
        self.PWMA.ChangeDutyCycle(30)
        self.PWMB.ChangeDutyCycle(30)
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.HIGH)

    def right(self):
        self.PWMA.ChangeDutyCycle(30)
        self.PWMB.ChangeDutyCycle(30)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.HIGH)
        GPIO.output(self.BIN1, GPIO.HIGH)
        GPIO.output(self.BIN2, GPIO.LOW)

    def setPWMA(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def setPWMB(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)

    def setMotor(self, left, right):
        if ((right >= 0) and (right <= 100)):
            GPIO.output(self.AIN1, GPIO.HIGH)
            GPIO.output(self.AIN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif ((right < 0) and (right >= -100)):
            GPIO.output(self.AIN1, GPIO.LOW)
            GPIO.output(self.AIN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if ((left >= 0) and (left <= 100)):
            GPIO.output(self.BIN1, GPIO.HIGH)
            GPIO.output(self.BIN2, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif ((left < 0) and (left >= -100)):
            GPIO.output(self.BIN1, GPIO.LOW)
            GPIO.output(self.BIN2, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)
