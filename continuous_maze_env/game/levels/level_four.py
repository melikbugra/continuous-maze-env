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


class LevelFour(BaseLevel):
    def setup_level(self, random_start: bool = False):
        super().__init__()

        self.inner_background.extend(
            [
                shapes.Rectangle(
                    x=GRID_SIZE * 0,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 0,
                    y=GRID_SIZE * 7,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 2,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 2,
                    y=GRID_SIZE * 7,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 4,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 1,
                    height=GRID_SIZE * 1,
                    color=WHITE,
                    batch=self.batch,
                ),
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
                    x=GRID_SIZE * 7,
                    y=GRID_SIZE * 8,
                    width=GRID_SIZE * 1,
                    height=GRID_SIZE * 1,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 8,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 8,
                    y=GRID_SIZE * 7,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 10,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 1,
                    height=GRID_SIZE * 1,
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
                    x=GRID_SIZE * 13,
                    y=GRID_SIZE * 8,
                    width=GRID_SIZE * 1,
                    height=GRID_SIZE * 1,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 14,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 14,
                    y=GRID_SIZE * 7,
                    width=GRID_SIZE * 2,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 16,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 1,
                    height=GRID_SIZE * 1,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 17,
                    y=GRID_SIZE * 5,
                    width=GRID_SIZE * 3,
                    height=GRID_SIZE * 2,
                    color=WHITE,
                    batch=self.batch,
                ),
                shapes.Rectangle(
                    x=GRID_SIZE * 17,
                    y=GRID_SIZE * 7,
                    width=GRID_SIZE * 3,
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
                    0, 0, 0, GRID_SIZE * 15, width=4, color=BLACK, batch=self.batch
                ),
                shapes.Line(
                    0,
                    GRID_SIZE * 15,
                    GRID_SIZE * 20,
                    GRID_SIZE * 15,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 20,
                    GRID_SIZE * 15,
                    GRID_SIZE * 20,
                    0,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 20, 0, 0, 0, width=4, color=BLACK, batch=self.batch
                ),
                # 1
                shapes.Line(
                    GRID_SIZE * 0,
                    GRID_SIZE * 9,
                    GRID_SIZE * 4,
                    GRID_SIZE * 9,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 4,
                    GRID_SIZE * 9,
                    GRID_SIZE * 4,
                    GRID_SIZE * 6,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 4,
                    GRID_SIZE * 6,
                    GRID_SIZE * 5,
                    GRID_SIZE * 6,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 5,
                    GRID_SIZE * 6,
                    GRID_SIZE * 5,
                    GRID_SIZE * 9,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 5,
                    GRID_SIZE * 9,
                    GRID_SIZE * 10,
                    GRID_SIZE * 9,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 10,
                    GRID_SIZE * 9,
                    GRID_SIZE * 10,
                    GRID_SIZE * 6,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 10,
                    GRID_SIZE * 6,
                    GRID_SIZE * 11,
                    GRID_SIZE * 6,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 11,
                    GRID_SIZE * 6,
                    GRID_SIZE * 11,
                    GRID_SIZE * 9,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 11,
                    GRID_SIZE * 9,
                    GRID_SIZE * 16,
                    GRID_SIZE * 9,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 16,
                    GRID_SIZE * 9,
                    GRID_SIZE * 16,
                    GRID_SIZE * 6,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 16,
                    GRID_SIZE * 6,
                    GRID_SIZE * 17,
                    GRID_SIZE * 6,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 17,
                    GRID_SIZE * 6,
                    GRID_SIZE * 17,
                    GRID_SIZE * 9,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 17,
                    GRID_SIZE * 9,
                    GRID_SIZE * 20,
                    GRID_SIZE * 9,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                # 2
                shapes.Line(
                    GRID_SIZE * 0,
                    GRID_SIZE * 5,
                    GRID_SIZE * 7,
                    GRID_SIZE * 5,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 7,
                    GRID_SIZE * 5,
                    GRID_SIZE * 7,
                    GRID_SIZE * 8,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 7,
                    GRID_SIZE * 8,
                    GRID_SIZE * 8,
                    GRID_SIZE * 8,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 8,
                    GRID_SIZE * 8,
                    GRID_SIZE * 8,
                    GRID_SIZE * 5,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 8,
                    GRID_SIZE * 5,
                    GRID_SIZE * 13,
                    GRID_SIZE * 5,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 13,
                    GRID_SIZE * 5,
                    GRID_SIZE * 13,
                    GRID_SIZE * 8,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 13,
                    GRID_SIZE * 8,
                    GRID_SIZE * 14,
                    GRID_SIZE * 8,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 14,
                    GRID_SIZE * 8,
                    GRID_SIZE * 14,
                    GRID_SIZE * 5,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
                shapes.Line(
                    GRID_SIZE * 14,
                    GRID_SIZE * 5,
                    GRID_SIZE * 20,
                    GRID_SIZE * 5,
                    width=4,
                    color=BLACK,
                    batch=self.batch,
                ),
            ]
        )

        if random_start:
            self.start_area = self.get_random_start_area()
        else:
            self.start_area = shapes.Rectangle(
                x=GRID_SIZE * 2 + 2,
                y=GRID_SIZE * 7 + 2,
                width=GRID_SIZE * 2 - 4,
                height=GRID_SIZE * 2 - 4,
                color=GREEN,
                batch=self.batch,
            )
        self.finish_area = shapes.Rectangle(
            x=GRID_SIZE * 0 + 2,
            y=GRID_SIZE * 7 + 2,
            width=GRID_SIZE * 2 - 4,
            height=GRID_SIZE * 2 - 4,
            color=END_ZONE,
            batch=self.batch,
        )

        self.player_start = (
            self.start_area.x + self.start_area.width / 2 - PLAYER_SIZE / 2,
            self.start_area.y + self.start_area.height / 2 - PLAYER_SIZE / 2,
        )

    def get_random_start_area(self):
        while True:
            x = random.randint(0, 18) * GRID_SIZE
            y = random.randint(0, 13) * GRID_SIZE
            start_rect = shapes.Rectangle(
                x=x + 2,
                y=y + 2,
                width=GRID_SIZE * 2 - 4,
                height=GRID_SIZE * 2 - 4,
                color=GREEN,
                batch=self.batch,
            )
            if not self.is_overlapping_finish_area(
                start_rect
            ) and not self.is_overlapping_walls(start_rect):
                return start_rect

    def is_overlapping_walls(self, rect: shapes.Rectangle):
        for line in self.wall_lines:
            if (
                rect.x - 4 < max(line.x, line.x2)
                and rect.x + rect.width + 4 > min(line.x, line.x2)
                and rect.y + 4 < max(line.y, line.y2)
                and rect.y + rect.height - 4 > min(line.y, line.y2)
            ):
                return True
        return False

    def is_overlapping_finish_area(self, rect: shapes.Rectangle):
        finish_x, finish_y, finish_w, finish_h = (
            GRID_SIZE * 18 + 2,
            GRID_SIZE * 0 + 2,
            GRID_SIZE * 2 - 4,
            GRID_SIZE * 2 - 4,
        )
        return not (
            rect.x + rect.width <= finish_x
            or rect.x >= finish_x + finish_w
            or rect.y + rect.height <= finish_y
            or rect.y >= finish_y + finish_h
        )

    def update(self):
        pass
