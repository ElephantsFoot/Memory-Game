import time

import ASUS.GPIO as GPIO

import random

import utils


class MemoryGame:
    def __init__(self):
        self.game_started = False
        self.menu()
        self.sequence = []

    def menu(self):
        GPIO.add_event_detect(utils.BUTTON, GPIO.FALLING, callback=self.start_game)
        diagonal_leds = [utils.UP_LEFT, utils.DOWN_LEFT, utils.DOWN_RIGHT, utils.UP_RIGHT]
        other_leds = [utils.UP, utils.DOWN, utils.LEFT, utils.RIGHT]
        while True:
            if self.game_started:
                break
            for led in diagonal_leds:
                GPIO.output(led, GPIO.HIGH)
            time.sleep(0.5)
            for led in diagonal_leds:
                GPIO.output(led, GPIO.LOW)
            for led in other_leds:
                GPIO.output(led, GPIO.HIGH)
            time.sleep(0.5)
            for led in other_leds:
                GPIO.output(led, GPIO.LOW)

    def start_game(self):
        self.game_started = True
        self.start_game_animation()
        GPIO.remove_event_detect(utils.BUTTON)
        while True:
            self.extend_sequence()
            correct_answer: bool = self.read_input_sequence()
            if not correct_answer:
                self.reset_game()
                break
        self.menu()

    def extend_sequence(self):
        self.sequence.append(random.choice(utils.LED_CIRCLE))
        self.sequence_animation()

    def read_input_sequence(self):
        for expected_led in self.sequence:
            x, y = utils.read_from_joystick()
            input_led = utils.convert_coords_into_led_number(x, y)
            if expected_led != input_led:
                return False
        return True

    def sequence_animation(self):
        for led in self.sequence:
            GPIO.output(led, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led, GPIO.LOW)

    def game_over_animation(self):
        for led in utils.LED_CIRCLE:
            GPIO.output(led, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(utils.UP, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(utils.UP_LEFT, GPIO.LOW)
        GPIO.output(utils.UP_RIGHT, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(utils.LEFT, GPIO.LOW)
        GPIO.output(utils.RIGHT, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(utils.DOWN_LEFT, GPIO.LOW)
        GPIO.output(utils.DOWN_RIGHT, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(utils.DOWN, GPIO.LOW)

    def start_game_animation(self):
        for led in utils.LED_CIRCLE:
            GPIO.output(led, GPIO.HIGH)
            time.sleep(0.1)
        for led in utils.LED_CIRCLE:
            GPIO.output(led, GPIO.LOW)

    def reset_game(self):
        self.game_over_animation()
        self.sequence.clear()
        self.game_started = False
        self.menu()

if __name__ == "__main__":
    try:
        game = MemoryGame()
    except KeyboardInterrupt:
        GPIO.cleanup()
