from pyglet.shapes import BorderedRectangle
from pyglet.graphics import Batch
from pyglet.window import key

from continuous_maze_env.game.utils.constants import (
    PLAYER_SIZE,
    PLAYER_SPEED,
    INTERVAL,
)


class Player:
    def __init__(self, start_x: int, start_y: int, batch: Batch):
        self.key_handler: key.KeyStateHandler = None

        self.object = BorderedRectangle(
            x=start_x,
            y=start_y,
            width=PLAYER_SIZE,
            height=PLAYER_SIZE,
            border=6,
            border_color=(127, 0, 0, 255),
            color=(10, 0, 255),
            batch=batch,
        )

    def update(
        self, horiztontal_action: float = None, vertical_action: float = None
    ) -> tuple[float, float]:
        total_dx = 0.0
        total_dy = 0.0

        # in game mode speed is constant, but in gymnasium env mode it depends on the actions
        if horiztontal_action is not None and vertical_action is not None:
            total_dx += float(horiztontal_action) * PLAYER_SPEED * INTERVAL
            total_dy += float(vertical_action) * PLAYER_SPEED * INTERVAL
        else:
            if self.key_handler is not None:
                if self.key_handler[key.LEFT]:
                    total_dx -= PLAYER_SPEED * INTERVAL
                if self.key_handler[key.RIGHT]:
                    total_dx += PLAYER_SPEED * INTERVAL
                if self.key_handler[key.UP]:
                    total_dy += PLAYER_SPEED * INTERVAL
                if self.key_handler[key.DOWN]:
                    total_dy -= PLAYER_SPEED * INTERVAL

        # The collision is resolved in Game.update; here we only compute the intended
        # new position for this physics update based on controls and INTERVAL.
        new_x = self.object.x + total_dx
        new_y = self.object.y + total_dy

        return float(new_x), float(new_y)
