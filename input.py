from dataclasses import dataclass
from pgzero.builtins import keyboard

@dataclass
class InputState:
    left: bool
    right: bool
    jump_pressed: bool
    fire_pressed: bool
    fire_held: bool

class InputHandler:
    def __init__(self):
        self.prev_space = False
        self.prev_up = False

    def capture_input(self):
        current_space = keyboard.space
        current_up = keyboard.up
        current_left = keyboard.left
        current_right = keyboard.right

        state = InputState(
            left=current_left,
            right=current_right,
            jump_pressed=current_up and not self.prev_up,
            fire_pressed=current_space and not self.prev_space,
            fire_held=current_space
        )

        self.prev_space = current_space
        self.prev_up = current_up
        return state