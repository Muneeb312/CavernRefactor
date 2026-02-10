# CavernRefactor


A modular refactor of the classic "Cavern" game using Pygame Zero.

## How to Run the Game

This project is structured as a standard Python package. You should run it directly with Python, which will handle the imports correctly.

**Install Dependencies** (if not already installed):
   ```bash
   pip install pgzero
   python main.py

The original cavern.py has been refactored into a modular architecture:

    src/app.py: Contains the main state machine that owns the current screen.

    src/screens/: Each game state (Menu, Play, GameOver) is now a separate class with its own update() and draw() methods.

    src/game.py: Contains the core Game logic, decoupled from the global scope. It is now a dependency injected into Screens and Actors.

    src/input.py: Centralized input processing. Raw Pygame Zero keyboard state is converted into an immutable InputState object once per frame.

    src/common.py: Holds shared constants and the GameContext service locator, which injects Pygame Zero globals (screen, sounds, keyboard) into the application at runtime to avoid circular import errors.


