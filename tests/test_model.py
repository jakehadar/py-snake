import pytest

from snake.model import SnakeModel
from snake.common import Frame, Point, DirectionOffset, BoundaryCollision, SelfCollision
from snake.config import GameConfig


@pytest.fixture
def config():
    config = GameConfig()
    config.solid_walls = True
    config.initial_food_count = 0
    config.food_increase_interval = 0
    return config


@pytest.fixture
def model(config):
    """Initial state (T0)."""
    frame = Frame(10, 10)
    m = SnakeModel(frame, config)
    return m


class TestSnakeModelInitialState:
    def test_length(self, model):
        assert len(model) == 1

    def test_score(self, model):
        assert model.score == 0

    def test_occupied_locations(self, model):
        assert {model.head_location} == set(model.occupied_locations)

    def test_empty_locaitons(self, model):
        assert model.head_location not in model.empty_locations

    def test_available_food_locations(self, model):
        assert model.available_food_locations == model.empty_locations


@pytest.fixture
def model2(model):
    """Initial state (T0) + 3 steps forward, where each spot had food."""
    model.face_up()
    model.food_locations.append(model.head_location + Point(0, 1))
    model.food_locations.append(model.head_location + Point(0, 2))
    model.food_locations.append(model.head_location + Point(0, 3))
    model.step()
    model.step()
    model.step()
    return model


class TestSnakeEatsAndGrows:
    def test_length(self, model2):
        assert len(model2) == 4

    def test_score(self, model2):
        assert model2.score == 3


class TestBoundaryCollision:
    def test_raises_scenario_1(self, config):
        model = SnakeModel(Frame(3, 3), config)
        model.face_up()
        with pytest.raises(BoundaryCollision):
            model.step()
            model.step()

    def test_raises_scenario_2(self, config):
        model = SnakeModel(Frame(3, 3), config)
        model.face_down()
        with pytest.raises(BoundaryCollision):
            model.step()
            model.step()

    def test_raises_scenario_3(self, config):
        model = SnakeModel(Frame(3, 3), config)
        model.face_left()
        with pytest.raises(BoundaryCollision):
            model.step()
            model.step()

    def test_raises_scenario_4(self, config):
        model = SnakeModel(Frame(3, 3), config)
        model.face_right()
        with pytest.raises(BoundaryCollision):
            model.step()
            model.step()


class TestSelfCollision:
    def test_valid_scenario_raises(self, model):
        """Snake turns into itself."""
        model.face_up()
        model.step(should_grow=True)
        model.step(should_grow=True)
        model.step(should_grow=True)
        model.face_right()
        model.step()
        model.face_down()
        model.step()
        model.face_left()
        with pytest.raises(SelfCollision):
            model.step()

    # The scenarios below should never raise

    def test_scenario_1a(self, model):
        model.face_up()
        model.step(should_grow=True)
        model.face_down()
        model.step()

    def test_scenario_1b(self, model):
        model.face_down()
        model.step(should_grow=True)
        model.face_up()
        model.step()

    def test_scenario_1c(self, model):
        model.face_left()
        model.step(should_grow=True)
        model.face_right()
        model.step()

    def test_scenario_1d(self, model):
        model.face_right()
        model.step(should_grow=True)
        model.face_left()
        model.step()

    def test_scenario_2a(self, model):
        model.face_up()
        model.step(should_grow=True)
        model.face_left()
        model.face_down()
        model.step()

    def test_scenario_2b(self, model):
        model.face_up()
        model.step(should_grow=True)
        model.face_right()
        model.face_down()
        model.step()

    def test_scenario_3a(self, model):
        model.face_down()
        model.step(should_grow=True)
        model.face_left()
        model.face_up()
        model.step()

    def test_scenario_3b(self, model):
        model.face_down()
        model.step(should_grow=True)
        model.face_right()
        model.face_up()
        model.step()

    def test_scenario_4a(self, model):
        model.face_left()
        model.step(should_grow=True)
        model.face_down()
        model.face_right()
        model.step()

    def test_scenario_4b(self, model):
        model.face_left()
        model.step(should_grow=True)
        model.face_up()
        model.face_right()
        model.step()

    def test_scenario_5a(self, model):
        model.face_right()
        model.step(should_grow=True)
        model.face_down()
        model.face_left()
        model.step()

    def test_scenario_5b(self, model):
        model.face_right()
        model.step(should_grow=True)
        model.face_up()
        model.face_left()
        model.step()
