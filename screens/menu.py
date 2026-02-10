from pgzero.builtins import screen
from src.game import Game
# Import inside method to avoid circular import if necessary, or just rely on Python's module caching
# But PlayScreen imports MenuScreen, so we must be careful.
# Strategy: Import 'PlayScreen' inside update.

class MenuScreen:
    def __init__(self, app):
        self.app = app
        self.bg_game = Game(app, player=None)

    def update(self, input_state):
        if input_state.fire_pressed:
            # Lazy import to break circular dependency
            from src.screens.play import PlayScreen
            self.app.change_screen(PlayScreen(self.app))
        else:
            self.bg_game.update()

    def draw(self):
        self.bg_game.draw()
        screen.blit("title", (0, 0))
        anim_frame = min(((self.bg_game.timer + 40) % 160) // 4, 9)
        screen.blit("space" + str(anim_frame), (130, 280))