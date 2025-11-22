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

    def update(self):
        pass
