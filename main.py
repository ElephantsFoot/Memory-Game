#!/usr/bin/python
import spidev
import time
import ASUS.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
BUTTON = 24
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Open SPI bus
spi = spidev.SpiDev()
spi.open(2,0)
spi.max_speed_hz=1000000

#define custom chip select
#this is done so we can use dozens of SPI devices on 1 bus
CS_ADC = 29
GPIO.setup(CS_ADC, GPIO.OUT)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel3008(channel):
  #below sends 00000001 1xxx0000 00000000 to the chip and records the response
  #xxx encodes 0-7, the channel selected for the transfer.
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def ConvertToVoltage(value, bitdepth, vref):
    return vref*(value/(2**bitdepth-1))

# Define delay between readings
delay = 0.1

def read_from_joystick():
  GPIO.output(CS_ADC, GPIO.LOW)
  y_value = ReadChannel3008(1)
  GPIO.output(CS_ADC, GPIO.HIGH)
  GPIO.output(CS_ADC, GPIO.LOW)
  x_value = ReadChannel3008(0)
  GPIO.output(CS_ADC, GPIO.HIGH)
  print(x_value, y_value)
  return x_value, y_value

UP = 3
UP_RIGHT = 22
RIGHT = 18
DOWN_RIGHT = 16
DOWN = 12
DOWN_LEFT = 11
LEFT = 7
UP_LEFT = 5
LED_CIRCLE = [UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT]

def light_leds(x, y):
    for led in LED_CIRCLE:
        GPIO.output(led, GPIO.LOW)
    if x > 600:
        if y > 600:
            GPIO.output(DOWN_RIGHT, GPIO.HIGH)
        if 500<=y<=600:
            GPIO.output(RIGHT, GPIO.HIGH)
        if y < 500:
            GPIO.output(UP_RIGHT, GPIO.HIGH)
    if x < 500:
        if y > 600:
            GPIO.output(DOWN_LEFT, GPIO.HIGH)
        if 500<=y<=600:
            GPIO.output(LEFT, GPIO.HIGH)
        if y < 500:
            GPIO.output(UP_LEFT, GPIO.HIGH)
    if 500 <=x <= 600:
        if y > 600:
            GPIO.output(DOWN, GPIO.HIGH)
        if y < 500:
            GPIO.output(UP, GPIO.HIGH)
for led in LED_CIRCLE:
    GPIO.setup(led, GPIO.OUT)

def blink_leds(times):
    for _ in range(times):
        for led in LED_CIRCLE:
            GPIO.output(led, GPIO.HIGH)
        time.sleep(0.1)
        for led in LED_CIRCLE:
            GPIO.output(led, GPIO.LOW)
        time.sleep(0.1)

try:
    while True:
        if not GPIO.input(BUTTON):
            blink_leds(5)
        x, y = read_from_joystick()
        light_leds(x, y)
        time.sleep(delay)
except KeyboardInterrupt:
    GPIO.cleanup()

