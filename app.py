from src.input import InputHandler
from src.screens.menu import MenuScreen

class CavernApp:
    def __init__(self):
        self.input_handler = InputHandler()
        self.screen = MenuScreen(self)

    def update(self):
        input_state = self.input_handler.capture_input()
        self.screen.update(input_state)

    def draw(self):
        self.screen.draw()

    def change_screen(self, new_screen):
        self.screen = new_screen