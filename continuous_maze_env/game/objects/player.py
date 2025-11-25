from pyglet.window import key

from continuous_maze_env.game.utils.constants import (
    PLAYER_SIZE,
    PLAYER_SPEED,
    INTERVAL,
)


class Player:
    def __init__(self, start_x: int, start_y: int, batch, shape_factory):
        self.key_handler: key.KeyStateHandler = None

        bordered_rect = shape_factory.BorderedRectangle
        self.object = bordered_rect(
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
    ) -> tuple[int, int]:
        dx = dy = 0

        # in game mode speed is constant, but in gymnasium env mode it depends on the actions
        if horiztontal_action is not None and vertical_action is not None:
            dx += horiztontal_action * PLAYER_SPEED * INTERVAL
            dy += vertical_action * PLAYER_SPEED * INTERVAL
        else:
            if self.key_handler is not None:
                if self.key_handler[key.LEFT]:
                    dx -= PLAYER_SPEED * INTERVAL
                if self.key_handler[key.RIGHT]:
                    dx += PLAYER_SPEED * INTERVAL
                if self.key_handler[key.UP]:
                    dy += PLAYER_SPEED * INTERVAL
                if self.key_handler[key.DOWN]:
                    dy -= PLAYER_SPEED * INTERVAL

        new_x = self.object.x + dx
        new_y = self.object.y + dy

        return new_x, new_y
