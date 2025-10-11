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
        # Parallel cache of axis-aligned bounding boxes for wall_lines
        # Each entry is a tuple (min_x, max_x, min_y, max_y)
        self.wall_aabbs: list[tuple[float, float, float, float]] = []
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

    def compute_wall_aabbs(self):
        """Compute and cache AABBs for all wall line segments.
        Should be called after self.wall_lines is populated.
        """
        aabbs: list[tuple[float, float, float, float]] = []
        for line in self.wall_lines:
            lx1 = line.x if line.x <= line.x2 else line.x2
            lx2 = line.x2 if line.x <= line.x2 else line.x
            ly1 = line.y if line.y <= line.y2 else line.y2
            ly2 = line.y2 if line.y <= line.y2 else line.y
            aabbs.append((lx1, lx2, ly1, ly2))
        self.wall_aabbs = aabbs
