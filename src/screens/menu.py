from src.common import GameContext
from src.game import Game

class MenuScreen:
    def __init__(self, app):
        self.app = app
        # Create a game for the background logic (no player)
        self.bg_game = Game(app, player=None)

    def update(self, input_state):
        if input_state.fire_pressed:
            # Import inside function to avoid circular import
            from src.screens.play import PlayScreen
            self.app.change_screen(PlayScreen(self.app))
        else:
            self.bg_game.update(input_state)

    def draw(self):
        self.bg_game.draw()
        
        # Access the screen via the context
        screen = GameContext.screen
        if screen:
            screen.blit("title", (0, 0))
            
            # Draw "Press SPACE" animation
            anim_frame = min(((self.bg_game.timer + 40) % 160) // 4, 9)
            screen.blit("space" + str(anim_frame), (130, 280))