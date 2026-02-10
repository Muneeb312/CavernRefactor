### `DESIGN.md`

```markdown
# Design Document

## 1. Screens Architecture

The game uses a **State Pattern** managed by the `CavernApp` class.

* **`CavernApp` (Context)**:
    * Holds the single active `self.screen` instance.
    * Delegates `update()` and `draw()` calls to the active screen.
    * Provides a `change_screen(new_screen)` method to handle transitions.

* **Screens (States)**:
    * **`MenuScreen`**: Handles the title loop. transitions to `PlayScreen` on input.
    * **`PlayScreen`**: Owns the `Game` instance. Handles the active gameplay loop and Pause logic. Transitions to `GameOverScreen` when lives < 0.
    * **`GameOverScreen`**: Renders the final state of the `Game` (background/score) with an overlay. Transitions back to `MenuScreen`.

## 2. Input Design

Input is decoupled from game logic to prevent "input lag" and ensure consistent behavior across entities.

* **`InputHandler`**:
    * Located in `src/input.py`.
    * Polled once per frame by `CavernApp`.
    * Tracks the *previous* frame's state to calculate "edges" (key presses vs. key holds).

* **`InputState` (Data Transfer Object)**:
    * An immutable dataclass passed down the hierarchy (`App` -> `Screen` -> `Game` -> `Player`).
    * **Fields**:
        * `left` / `right`: Boolean (Held state).
        * `fire_held`: Boolean (Held state for "blowing" bubbles further).
        * `jump_pressed`: Boolean (True only on the exact frame pressed).
        * `fire_pressed`: Boolean (True only on the exact frame pressed).
        * `pause_pressed`: Boolean (True only on the exact frame pressed).

## 3. Pause Implementation

The Pause feature is implemented entirely within the `PlayScreen` to ensure it isolates gameplay execution without stopping the application loop.

* **State Tracking**: `PlayScreen` maintains a simple boolean flag: `self.paused`.
* **Toggling**:
    * Inside `PlayScreen.update()`, we check `input_state.pause_pressed`.
    * If detected, `self.paused` is toggled.
* **Execution Flow**:
    * **If Paused**: The `update()` method returns immediately. No calls are made to `self.game.update()`, freezing all actors, timers, and physics.
    * **If Active**: `self.game.update()` is called normally.
* **Rendering**:
    * `draw()` is **always** called. This ensures the game world remains visible while frozen.
    * If `self.paused` is true, an additional `draw_text("PAUSED", ...)` call is made to render the overlay on top of the frozen game world.