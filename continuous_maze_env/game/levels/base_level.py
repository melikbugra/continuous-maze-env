import time
import math

import pyglet
from pyglet.shapes import Rectangle, Circle, Line


class BaseLevel:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.black_stripes = []
        self.start_area = None
        self.finish_area = None
        self.wall_lines = []
        # Parallel cache of axis-aligned bounding boxes for wall_lines
        # Each entry is a tuple (min_x, max_x, min_y, max_y)
        self.wall_aabbs = []
        # Spatial hash grid: maps (ix, iy) -> list of wall line indices
        self.wall_grid = {}
        self.grid_cell_size = None
        self.inner_background = []
        self.obstacles = []
        self.obstacle_inners = []
        self.player_start = None

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
        aabbs = []
        for line in self.wall_lines:
            lx1 = line.x if line.x <= line.x2 else line.x2
            lx2 = line.x2 if line.x <= line.x2 else line.x
            ly1 = line.y if line.y <= line.y2 else line.y2
            ly2 = line.y2 if line.y <= line.y2 else line.y
            aabbs.append((lx1, lx2, ly1, ly2))
        self.wall_aabbs = aabbs

    def build_spatial_index(self, cell_size: float):
        """Build a simple uniform grid (spatial hash) over wall line AABBs.
        Lines are inserted into all cells overlapped by their AABB.
        Call after `wall_lines` (and preferably `wall_aabbs`) is set.
        """
        if not self.wall_lines:
            self.wall_grid = {}
            self.grid_cell_size = cell_size
            return

        # Ensure we have AABBs to compute grid coverage
        if not self.wall_aabbs or len(self.wall_aabbs) != len(self.wall_lines):
            self.compute_wall_aabbs()

        grid = {}
        inv_cs = 1.0 / float(cell_size) if cell_size else 1.0
        for idx, (min_x, max_x, min_y, max_y) in enumerate(self.wall_aabbs):
            ix1 = int(math.floor(min_x * inv_cs))
            ix2 = int(math.floor(max_x * inv_cs))
            iy1 = int(math.floor(min_y * inv_cs))
            iy2 = int(math.floor(max_y * inv_cs))
            for ix in range(ix1, ix2 + 1):
                for iy in range(iy1, iy2 + 1):
                    grid.setdefault((ix, iy), []).append(idx)
        self.wall_grid = grid
        self.grid_cell_size = float(cell_size)
