from src.game import Game
from src.entities.actors import Player
from src.screens.game_over import GameOverScreen

class PlayScreen:
    def __init__(self, app):
        self.app = app
        p = Player(None)
        self.game = Game(app, player=p)

    def update(self, input_state):
        if self.game.player.lives < 0:
            self.game.play_sound("over")
            self.app.change_screen(GameOverScreen(self.app, self.game))
        else:
            self.game.update(input_state)

    def draw(self):
        self.game.draw()
        self.game.draw_status()