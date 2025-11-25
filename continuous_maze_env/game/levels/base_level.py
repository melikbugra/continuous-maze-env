import random
import time

from continuous_maze_env.game.utils.colors import GREEN
from continuous_maze_env.game.utils.constants import GRID_SIZE


class BaseLevel:
    def __init__(self):
        self.shape_factory = None
        self.shapes = None
        self.batch = None
        self.black_stripes = []
        self.start_area = None
        self.finish_area = None
        self.wall_lines = []
        self.inner_background = []
        self.obstacles = []
        self.obstacle_inners = []
        self.player_start = None

        self.overlap_time = None
        self.start_time = time.time()

    def attach_factory(self, shape_factory):
        self.shape_factory = shape_factory
        self.shapes = shape_factory.shapes

    def begin_setup(self):
        if self.shape_factory is None:
            raise RuntimeError("Shape factory must be attached before setup")
        self.batch = self.shape_factory.create_batch()
        self.black_stripes = []
        self.start_area = None
        self.finish_area = None
        self.wall_lines = []
        self.inner_background = []
        self.obstacles = []
        self.obstacle_inners = []
        self.player_start = None

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
        start_area = self.shapes.Rectangle(
            x=random_rectangle.x + 2,
            y=random_rectangle.y + 2,
            width=GRID_SIZE * 2 - 4,
            height=GRID_SIZE * 2 - 4,
            color=GREEN,
            batch=self.batch,
        )

        return start_area

    def rect_overlap(self, rect1, rect2):
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
