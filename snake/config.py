class GameConfig:
    width = 25
    height = 10
    initial_speed = 3.0
    max_speed = 30
    speed_increase_factor = 0.15
    solid_walls = True

    # Amount of food initially displayed on screen.
    initial_food_count = 1
    max_food_count = 5

    # Increment food_count for every N points scored.
    # (Set this to 0 to keep food_count unchanged).
    food_increase_interval = 10
