import sys

from kbhit import KBHit

from engine import GameEngine
from model import SnakeModel
from controller import SnakeModelController
from view import Canvas
from common import Frame, GameConfig, SelfCollision, BoundaryCollision


class Game(GameEngine):
    def __init__(self, config, kb_hit_cls=KBHit):
        super().__init__(config.speed)
        self.config = config
        self.frame = Frame(config.width, config.height)
        self.model = SnakeModel(self.frame, config.solid_walls)
        self.canvas = Canvas(self.frame, self.model)  # TODO: make canvas less coupled to model
        self.snake_controller = SnakeModelController(self.model)

        self.kb = kb_hit_cls()
        self.last_key = None
        self.status_message = ""

    def run(self):
        try:
            self.start_game()
        except KeyboardInterrupt:
            self.stop_game()
        except Exception:
            raise

    def game_should_update_frame(self):
        last_key = self.last_key

        if self.elapsed_time < 1.0:
            self.canvas.render("Ready.")
            return

        if self.elapsed_time < 2.0:
            self.canvas.render("Set.")
            return

        snake_should_grow = False
        if last_key is not None:
            if last_key == 'up':
                self.snake_controller.face_up()
            elif last_key == 'down':
                self.snake_controller.face_down()
            elif last_key == 'left':
                self.snake_controller.face_left()
            elif last_key == 'right':
                self.snake_controller.face_right()
            elif last_key == 'g':
                snake_should_grow = True

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

        self.last_key = None
        self.kb._lock = False

    def game_should_capture_input(self):
        if self.kb.kbhit():
            self.last_key = self.kb.getch()

    def game_did_end(self):
        self.canvas.render("Game Over.")
        if self.status_message:
            print(self.status_message)


def testme():
    from kbhit import KBHitSequencer
    def kb_factory():
        return KBHitSequencer(iter([None, 'up', 'g', 'g', 'g', 'g', 'g', 'g', 'right', 'down', 'left']))

    config = GameConfig()
    config.solid_walls = True
    game = Game(config=config, kb_hit_cls=kb_factory)
    game.run()


def main():
    from common import GameConfig

    if len(sys.argv) == 3:
        width, height = sys.argv[1:]
        config = GameConfig(int(width), int(height), solid_walls=True)

    elif len(sys.argv) > 3:
        width, height, speed = sys.argv[1:4]
        config = GameConfig(int(width), int(height), float(speed), solid_walls=True)

    else:
        config = GameConfig()

    game = Game(config=config)
    game.run()
    return 0


if __name__ == '__main__':
    sys.exit(main())
