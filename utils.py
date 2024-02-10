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
#this is done, so we can use dozens of SPI devices on 1 bus
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

def read_from_joystick() -> (int, int):
  GPIO.output(CS_ADC, GPIO.LOW)
  y_value = ReadChannel3008(1)
  GPIO.output(CS_ADC, GPIO.HIGH)
  GPIO.output(CS_ADC, GPIO.LOW)
  x_value = ReadChannel3008(0)
  GPIO.output(CS_ADC, GPIO.HIGH)
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

def convert_coords_into_led_number(x, y) -> int | None :
    for led in LED_CIRCLE:
        GPIO.output(led, GPIO.LOW)
    result_led = None
    if x > 1000:
        return None
    if x > 750:
        if y > 750:
            result_led = DOWN_RIGHT
        if 350<=y<=750:
            result_led = RIGHT
        if y < 350:
            result_led = UP_RIGHT
    if x < 350:
        if y > 750:
            result_led = DOWN_LEFT
        if 350<=y<=750:
            result_led = LEFT
        if y < 350:
            result_led = UP_LEFT
    if 350 <=x <= 750:
        if y > 750:
            result_led = DOWN
        if y < 350:
            result_led = UP

    if result_led:
        GPIO.output(result_led, GPIO.HIGH)
    time.sleep(0.5)
    if result_led:
        GPIO.output(result_led, GPIO.LOW)
    return result_led

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
