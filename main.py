import pgzrun
import pygame
import sys
from pgzero.builtins import music
from src.app import CavernApp
from src.common import WIDTH, HEIGHT, TITLE

# Python version check
if sys.version_info < (3,5):
    print("This game requires at least version 3.5 of Python.")
    sys.exit()

# Setup App
app = CavernApp()

def update():
    app.update()

def draw():
    app.draw()

# Audio Init
try:
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 1024)
    music.play("theme")
    music.set_volume(0.3)
except Exception:
    pass

pgzrun.go()