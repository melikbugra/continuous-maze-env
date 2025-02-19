import time

import pyglet
from pyglet.shapes import Rectangle, Circle, Line


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

    def update(self):
        """
        Abstract method that each level should implement to update elements.
        """
        raise NotImplementedError("Each level must define its update.")
