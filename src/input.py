from dataclasses import dataclass
# REMOVE: from pgzero.builtins import keyboard
from src.common import GameContext # <--- Import context

@dataclass
class InputState:
    left: bool
    right: bool
    jump_pressed: bool
    fire_pressed: bool
    fire_held: bool
    pause_pressed: bool

class InputHandler:
    def __init__(self):
        self.prev_space = False
        self.prev_up = False
        self.prev_p = False

    def capture_input(self):
        # Use GameContext.keyboard
        k = GameContext.keyboard
        if not k: return InputState(False, False, False, False, False, False) # Safety check

        current_space = k.space
        current_up = k.up
        current_left = k.left
        current_right = k.right
        current_p = k.p

        state = InputState(
            left=current_left,
            right=current_right,
            jump_pressed=current_up and not self.prev_up,
            fire_pressed=current_space and not self.prev_space,
            fire_held=current_space,
            pause_pressed=current_p and not self.prev_p
        )

        self.prev_space = current_space
        self.prev_up = current_up
        self.prev_p = current_p
        return state