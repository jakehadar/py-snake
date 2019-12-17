from typing import NamedTuple
from threading import Thread

from pynput.keyboard import Key, Listener

from snake.engine import GameEngine
from snake.model import SnakeModel
from snake.controller import SnakeModelController
from snake.view import Canvas
from snake.common import Frame, SelfCollision, BoundaryCollision, GameOver


class Game(GameEngine):
    def __init__(self, config):
        super().__init__(config.initial_speed)
        self.config = config
        self.frame = Frame(config.width, config.height)
        self.model = SnakeModel(self.frame, config)
        self.canvas = Canvas(self.frame, self.model, self)  # TODO: make canvas less coupled to model
        self.snake_controller = SnakeModelController(self.model)

        self.last_key = None
        self.status_message = ""

    def run(self):
        try:
            self.start_game()
        except KeyboardInterrupt:
            self.stop_game()
        except Exception:
            raise

    def game_will_begin(self):
        def target():
            def on_press(key):
                self.last_key = key

            with Listener(on_press=on_press) as listener:
                listener.join()

        t = Thread(target=target)
        t.start()

    def game_should_update_frame(self):
        last_key = self.last_key

        if self.elapsed_time < 1.0:
            self.canvas.render("Ready.")
            return

        if self.elapsed_time < 2.0:
            self.canvas.render("Set.")
            return

        if self.speed < self.config.max_speed:
            self.speed = self.initial_speed + (self.model.score * self.config.speed_increase_factor)

        snake_should_grow = False
        if last_key is not None:
            if last_key == Key.up:
                self.snake_controller.face_up()
            elif last_key == Key.down:
                self.snake_controller.face_down()
            elif last_key == Key.left:
                self.snake_controller.face_left()
            elif last_key == Key.right:
                self.snake_controller.face_right()
            elif last_key == Key.esc:
                self.stop_game()

        try:
            self.snake_controller.step(snake_should_grow)
        except SelfCollision:
            self.status_message = "Collision with self!"
            self.stop_game()
        except BoundaryCollision:
            self.status_message = "Collision with wall!"
            self.stop_game()
        else:
            overlay_text = None
            if self.elapsed_time < 3.0:
                overlay_text = 'GO!'

            self.canvas.render(overlay_text)

    def game_should_capture_input(self):
        pass

    def game_did_end(self):
        self.canvas.render("Game Over.")
        if self.status_message:
            print(self.status_message)

        raise GameOver


class GameConfig(NamedTuple):
    width: int = 25
    height: int = 10
    initial_speed: float = 3.0
    max_speed: float = 30
    speed_increase_factor = 0.15
    solid_walls: bool = True

    # Amount of food initially displayed on screen.
    initial_food_count: int = 1
    max_food_count: int = 5

    # Increment food_count for every N points scored.
    # (Set this to 0 to keep food_count unchanged).
    food_increase_interval: int = 10
