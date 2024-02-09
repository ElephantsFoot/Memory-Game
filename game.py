import time

import ASUS.GPIO as GPIO

import random

import utils


class MenuState:
    def __init__(self, game):
        self.game = game
        GPIO.add_event_detect(utils.BUTTON, GPIO.FALLING, callback=self.start_game)
        self.diagonal_leds = [utils.UP_LEFT, utils.DOWN_LEFT, utils.DOWN_RIGHT, utils.UP_RIGHT]
        self.other_leds = [utils.UP, utils.DOWN, utils.LEFT, utils.RIGHT]

    def execute(self):
        for led in self.diagonal_leds:
            GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        for led in self.diagonal_leds:
            GPIO.output(led, GPIO.LOW)
        for led in self.other_leds:
            GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        for led in self.other_leds:
            GPIO.output(led, GPIO.LOW)

    def start_game(self):
        for led in utils.LED_CIRCLE:
            GPIO.output(led, GPIO.LOW)
        self.game.state = PlayState(game)


class PlayState:
    def __init__(self, game):
        self.game = game
        self.sequence = []
        self.start_game_animation()

    def start_game_animation(self):
        for led in utils.LED_CIRCLE:
            GPIO.output(led, GPIO.HIGH)
            time.sleep(0.1)
        for led in utils.LED_CIRCLE:
            GPIO.output(led, GPIO.LOW)

    def execute(self):
        self.extend_sequence()
        correct_answer: bool = self.read_input_sequence()
        if not correct_answer:
            self.reset_game()

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


    def reset_game(self):
        self.game_over_animation()
        self.game.state = MenuState(self.game)


class MemoryGame:
    def __init__(self):
        self.game_started = False
        self.state = MenuState(self)

    def play(self):
        while True:
            self.state.execute()



if __name__ == "__main__":
    try:
        game = MemoryGame()
        game.play()
    except KeyboardInterrupt:
        GPIO.cleanup()
