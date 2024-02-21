# Memory Game
It is a fun embedded systems project that will teach you how to read input values from joystick.

## Required components
- Raspberry Pi (Tinker Board, Orange Pi, Banana Pi…)
- a breadboard
- GPIO breakout expansion board
- 8 LEDs
- a good joystick
- analog-to-digital converter (MCP3008)
- a bunch of wires

## Gameflow
1. Play menu animation waiting for the player to start the game. To start the game one should press a joystick button.
2. Each round is started by an animation of a spinning circle. The sequence is presented to the player.
3. Using the joystick player inputs the sequence. If the sequence was input correctly then extend the sequence.
4. If the player made an error a game over animation is played. Go back to menu.

## Schema
ToDo

## Code usage
```
sudo python game.py
```
I had to use `sudo` to have rights to access SPI interface to read the signal from MCP3008.
