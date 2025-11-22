import random
import time

import pyglet
from pyglet.shapes import Rectangle, Circle, Line

from continuous_maze_env.game.utils.colors import GREEN
from continuous_maze_env.game.utils.constants import GRID_SIZE


class BaseLevel:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.black_stripes: list[Rectangle] = []
        self.start_area: Rectangle = None
        self.finish_area: Rectangle = None
        self.wall_lines: list[Line] = []
        self.inner_background: list[Rectangle] = []
        self.obstacles: list[Circle] = []
        self.obstacle_inners: list[Circle] = []
        self.player_start: tuple[int, int] = None

        self.overlap_time = None
        self.start_time = time.time()

    def setup_level(self, random_start: bool = False):
        """
        Abstract method that each level should implement to initialize elements.
        """
        raise NotImplementedError("Each level must define its setup.")

    def get_random_start_area(self):
        while True:
            # Randomly select one of the inner background rectangles
            random_rectangle = random.choice(self.inner_background)

            if (
                random_rectangle.width < GRID_SIZE * 2
                or random_rectangle.height < GRID_SIZE * 2
            ):
                continue

            # If the random rectangle does not overlap with the finish area,break
            if not self.rect_overlap(random_rectangle, self.finish_area):
                break
        # Create a start area rectangle that has the same x, y, but height and width of 2
        start_area = Rectangle(
            x=random_rectangle.x + 2,
            y=random_rectangle.y + 2,
            width=GRID_SIZE * 2 - 4,
            height=GRID_SIZE * 2 - 4,
            color=GREEN,
            batch=self.batch,
        )

        return start_area

    def rect_overlap(self, rect1: Rectangle, rect2: Rectangle):
        return not (
            rect1.x + rect1.width <= rect2.x
            or rect2.x + rect2.width <= rect1.x
            or rect1.y + rect1.height <= rect2.y
            or rect2.y + rect2.height <= rect1.y
        )

    def update(self):
        """
        Abstract method that each level should implement to update elements.
        """
        raise NotImplementedError("Each level must define its update.")
