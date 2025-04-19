import pyglet
from pyglet import shapes
from pyglet.window import key, Window
from continuous_maze_env.game.levels.level_one import LevelOne
from continuous_maze_env.game.levels.level_two import LevelTwo
from continuous_maze_env.game.levels.level_three import LevelThree
from continuous_maze_env.game.levels.level_four import LevelFour
from continuous_maze_env.game.levels.base_level import BaseLevel
import time
import numpy as np
from pyglet.gl import glClearColor
from pyglet import gl

from continuous_maze_env.game.utils.functions import (
    line_segments_intersect,
    rectangle_circle_overlap,
    rectangle_inside,
)
from continuous_maze_env.game.utils.constants import (
    INTERVAL,
    PLAYER_SPEED,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    RENDER_SCALE,
)
from continuous_maze_env.game.objects.player import Player

LEVELS = {
    "level_one": LevelOne,
    "level_two": LevelTwo,
    "level_three": LevelThree,
    "level_four": LevelFour,
}


class ContinuousMazeGame:
    def __init__(
        self,
        level: str,
        random_start: bool = False,
        max_steps: int = 2500,
        constant_penalty: bool = False,
    ):
        self.constant_penalty = constant_penalty
        self.window = Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, visible=False)
        glClearColor(0.6667, 0.6471, 1, 1)
        self.level: BaseLevel = LEVELS[level]()
        self.random_start = random_start
        self.eliminated = False
        self.max_steps = max_steps
        self.setup_level_and_player(random_start=self.random_start)

    def setup_rendering(self):
        # Re-create the window if it doesn't exist
        if self.window is None:
            self.window = Window(
                width=WINDOW_WIDTH, height=WINDOW_HEIGHT, visible=False
            )
            glClearColor(0.6667, 0.6471, 1, 1)
            # Re-setup the level and player since they might depend on the window
            self.setup_level_and_player(random_start=self.random_start)

        # make the window visible
        self.window.set_visible()

        pyglet.clock.schedule_interval(self.update, INTERVAL)

        @self.window.event
        def on_draw():
            self.window.clear()
            if self.level and self.level.batch:
                self.level.batch.draw()
                pass

    def setup_key_handler(self):
        self.player.key_handler = key.KeyStateHandler()
        self.window.push_handlers(self.player.key_handler)

    def play(self):
        self.run()

    def run(self):
        if not self.window:
            self.setup_rendering()
        if not self.player.key_handler:
            self.setup_key_handler()

        pyglet.app.run()

    def update(
        self,
        interval: float,
        horiztontal_action: float = None,
        vertical_action: float = None,
    ):
        player_new_x, player_new_y = self.player.update(
            horiztontal_action, vertical_action
        )

        collision = self.check_collision(player_new_x, player_new_y)

        if collision == 0:
            self.player.object.x = player_new_x
            self.player.object.y = player_new_y
            self.eliminated = False

        elif collision == 1:
            # Try moving along x-axis only
            if not self.check_collision(player_new_x, self.player.object.y):
                self.player.object.x = player_new_x
            # Try moving along y-axis only
            if not self.check_collision(self.player.object.x, player_new_y):
                self.player.object.y = player_new_y
        elif collision == 2:
            print("You lose!")
            self.eliminated = True

        self.level.update()

        # Check if player is completely inside the finish area
        reward, finished = self.player_in_finish_area(interval)
        if collision == 2:
            reward = -1
            finished = True
        else:
            if not finished:
                if self.constant_penalty:
                    reward = -0.001
                else:
                    reward = -1 / self.max_steps
        self.reward = reward
        self.finished = finished

        # import matplotlib.pyplot as plt

        # print(self.get_window_image())

        # plt.imshow(self.get_window_image(), cmap="gray")
        # plt.show()

        if finished or self.eliminated:
            self.reset_game()

    def step(
        self,
        horiztontal_action: float = None,
        vertical_action: float = None,
    ):
        self.update(
            interval=INTERVAL,
            horiztontal_action=horiztontal_action,
            vertical_action=vertical_action,
        )

    def setup_level_and_player(self, random_start: bool = False):
        self.level.setup_level(random_start=random_start)
        self.player = Player(
            self.level.player_start[0], self.level.player_start[1], self.level.batch
        )
        if self.window:
            self.setup_key_handler()

    def check_collision(self, new_x, new_y):
        """
        Check if the player's rectangle at position (new_x, new_y)
        collides with any of the wall lines.
        """
        # Get the corners of the player's rectangle
        player_rect = {
            "left": new_x,
            "right": new_x + self.player.object.width,
            "bottom": new_y,
            "top": new_y + self.player.object.height,
        }

        # Get the four edges (line segments) of the player's rectangle
        player_edges = [
            # Bottom edge
            (
                (player_rect["left"], player_rect["bottom"]),
                (player_rect["right"], player_rect["bottom"]),
            ),
            # Right edge
            (
                (player_rect["right"], player_rect["bottom"]),
                (player_rect["right"], player_rect["top"]),
            ),
            # Top edge
            (
                (player_rect["right"], player_rect["top"]),
                (player_rect["left"], player_rect["top"]),
            ),
            # Left edge
            (
                (player_rect["left"], player_rect["top"]),
                (player_rect["left"], player_rect["bottom"]),
            ),
        ]

        # Check collision with each wall line
        for line in self.level.wall_lines:
            if line.y == line.y2:
                # wall_line = ((line.x + 2, line.y), (line.x2 - 2, line.y2))
                wall_line = ((line.x, line.y), (line.x2, line.y2))
            else:
                wall_line = ((line.x, line.y), (line.x2, line.y2))
            for edge in player_edges:
                if line_segments_intersect(
                    edge[0], edge[1], wall_line[0], wall_line[1]
                ):
                    return 1  # collision with wall

        # Check collision with enemies
        for obstacle in self.level.obstacles:
            if rectangle_circle_overlap(player_rect, obstacle):
                return 2  # collision with enemy

        return 0  # no collision

    def reset_game(self):
        self.setup_level_and_player(random_start=self.random_start)

    def player_in_finish_area(self, interval: float = INTERVAL):
        reward = 0
        finished = False
        if rectangle_inside(self.player.object, self.level.finish_area):
            # print("Congratulations! You've completed the level!")
            if self.constant_penalty:
                reward = 10
            else:
                reward = 1
            finished = True
        return reward, finished

    def get_window_image(self, resize_shape=None) -> np.ndarray:
        try:
            # Make sure we're using the correct context
            if not hasattr(self, "_gl_context"):
                # Create a new window and context if needed
                self.window = Window(
                    width=WINDOW_WIDTH, height=WINDOW_HEIGHT, visible=False
                )
                self._gl_context = self.window.context
                glClearColor(0.6667, 0.6471, 1, 1)

                # Reinitialize the level and player if needed
                self.setup_level_and_player(random_start=self.random_start)

            # Make our context current
            self.window.switch_to()

            # Clear and draw
            self.window.clear()
            if self.level and self.level.batch:
                self.level.batch.draw()

            # Ensure all commands are executed
            self.window.flip()

            # Read pixels
            width, height = self.window.get_size()
            buffer = (gl.GLubyte * (width * height * 3))()
            gl.glReadPixels(0, 0, width, height, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, buffer)

            # Convert to numpy array
            arr = np.frombuffer(buffer, dtype=np.uint8)
            arr = arr.reshape((height, width, 3))
            arr = np.flip(arr, axis=0).copy()

            # Resize if needed
            if resize_shape is not None:
                from PIL import Image

                img = Image.fromarray(arr)
                img = img.resize(resize_shape[:2][::-1], Image.Resampling.BILINEAR)
                arr = np.array(img)

            return arr.astype(np.uint8)

        except Exception as e:
            print(f"Error in get_window_image: {e}")
            # Clean up and try one more time
            if hasattr(self, "_gl_context"):
                delattr(self, "_gl_context")
            if hasattr(self, "window"):
                self.window.close()
                self.window = None
            return np.zeros(
                resize_shape if resize_shape else (WINDOW_HEIGHT, WINDOW_WIDTH, 3),
                dtype=np.uint8,
            )

    def get_reward(self):
        return self.reward

    def is_done(self):
        return self.finished or self.eliminated
