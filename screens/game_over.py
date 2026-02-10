from pgzero.builtins import screen

class GameOverScreen:
    def __init__(self, app, previous_game):
        self.app = app
        self.game = previous_game

    def update(self, input_state):
        if input_state.fire_pressed:
            from src.screens.menu import MenuScreen
            self.app.change_screen(MenuScreen(self.app))

    def draw(self):
        self.game.draw()
        self.game.draw_status()
        screen.blit("over", (0, 0))