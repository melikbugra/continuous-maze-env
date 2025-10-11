import time
import math
import random

from continuous_maze_env.game.levels.base_level import BaseLevel
from continuous_maze_env.game.utils.constants import PLAYER_SIZE, GRID_SIZE
from pyglet import shapes
from continuous_maze_env.game.utils.colors import (
    BLACK,
    GREEN,
    LIGHT_BLUE,
    WHITE,
    BACKGROUND,
    END_ZONE,
)


class LevelOne(BaseLevel):
    def setup_level(self, random_start: bool = False):
        super().__init__()

        self.inner_background.extend(
            [
                shapes.Rectangle(
                    x=GRID_SIZE * 5,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 5,
                    y=GRID_SIZE * 7,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 5,
                    y=GRID_SIZE * 9,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 7,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 7,
                    y=GRID_SIZE * 7,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 7,
                    y=GRID_SIZE * 9,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 9,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 9,
                    y=GRID_SIZE * 7,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 9,
                    y=GRID_SIZE * 9,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 11,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 11,
                    y=GRID_SIZE * 7,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 11,
                    y=GRID_SIZE * 9,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 13,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 13,
                    y=GRID_SIZE * 7,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 13,
                    y=GRID_SIZE * 9,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
            ]
        )

        self.wall_lines.extend(
            [
                # 0
                shapes.Line(
                    GRID_SIZE * 5,
                    GRID_SIZE * 5,
                    GRID_SIZE * 5,
                    GRID_SIZE * 11,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 5,
                    GRID_SIZE * 11,
                    GRID_SIZE * 15,
                    GRID_SIZE * 11,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 15,
                    GRID_SIZE * 11,
                    GRID_SIZE * 15,
                    GRID_SIZE * 5,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 15,
                    GRID_SIZE * 5,
                    GRID_SIZE * 5,
                    GRID_SIZE * 5,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
            ]
        )
        # Precompute AABBs for faster collision checks and build spatial index
        self.compute_wall_aabbs()
        from continuous_maze_env.game.utils.constants import GRID_SIZE

        self.build_spatial_index(cell_size=GRID_SIZE)

        self.finish_area = shapes.Rectangle(
            x=GRID_SIZE * 13 + 2,
            y=GRID_SIZE * 9 + 2,
            width=GRID_SIZE * 2 - 4,
            height=GRID_SIZE * 2 - 4,
            color=END_ZONE,
            batch=self.batch,
        )

        if random_start:
            self.start_area = self.get_random_start_area()
        else:
            self.start_area = shapes.Rectangle(
                x=GRID_SIZE * 11 + 2,
                y=GRID_SIZE * 7 + 2,
                width=GRID_SIZE * 2 - 4,
                height=GRID_SIZE * 2 - 4,
                color=GREEN,
                batch=self.batch,
            )

        self.player_start = (
            self.start_area.x + self.start_area.width / 2 - PLAYER_SIZE / 2,
            self.start_area.y + self.start_area.height / 2 - PLAYER_SIZE / 2,
        )

    def get_random_start_area(self):
        while True:
            # Randomly select one of the inner background rectangles
            random_rectangle = random.choice(self.inner_background)

            # If the random rectangle does not overlap with the finish area,break
            if not rect_overlap(random_rectangle, self.finish_area):
                break
        # Create a start area rectangle that has the same x, y, but height and width of 2
        start_area = shapes.Rectangle(
            x=random_rectangle.x + 2,
            y=random_rectangle.y + 2,
            width=GRID_SIZE * 2 - 4,
            height=GRID_SIZE * 2 - 4,
            color=GREEN,
            batch=self.batch,
        )

        return start_area

    def update(self):
        pass


def rect_overlap(rect1, rect2):
    return not (
        rect1.x + rect1.width <= rect2.x
        or rect2.x + rect2.width <= rect1.x
        or rect1.y + rect1.height <= rect2.y
        or rect2.y + rect2.height <= rect1.y
    )
