import os

import pyglet

_PYGLET_ERROR: Exception | None = None
try:
    from pyglet.window import key, Window
    from pyglet.gl import glClearColor
    from pyglet import gl
except Exception as exc:  # pragma: no cover - import guard triggers headless
    key = None
    Window = None
    glClearColor = None
    gl = None
    _PYGLET_ERROR = exc

from continuous_maze_env.game.levels.level_one import LevelOne
from continuous_maze_env.game.levels.level_two import LevelTwo
from continuous_maze_env.game.levels.level_three import LevelThree
from continuous_maze_env.game.levels.level_four import LevelFour
from continuous_maze_env.game.levels.level_five import LevelFive
from continuous_maze_env.game.levels.level_six import LevelSix
from continuous_maze_env.game.levels.base_level import BaseLevel
import time
import numpy as np

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
from continuous_maze_env.game.utils.shape_factory import ShapeFactory

LEVELS = {
    "level_one": LevelOne,
    "level_two": LevelTwo,
    "level_three": LevelThree,
    "level_four": LevelFour,
    "level_five": LevelFive,
    "level_six": LevelSix,
}


def _require_pyglet(feature: str = "Rendering") -> None:
    if _PYGLET_ERROR is None:
        return
    raise RuntimeError(
        f"{feature} requires pyglet with a working display. Set render_mode=None for"
        " headless training or install a virtual display (e.g. Xvfb)."
    ) from _PYGLET_ERROR


class ContinuousMazeGame:
    def __init__(
        self,
        level: str,
        random_start: bool = False,
        max_steps: int = 2500,
        constant_penalty: bool = False,
        headless: bool = False,
        dense_reward: bool = False,
    ):
        """Core game object.

        headless: when True, avoids creating a Pyglet window and GL context until
        an explicit render or image capture is requested. This substantially
        speeds up training loops that don't need pixels.
        """
        self.constant_penalty = constant_penalty
        self.dense_reward = dense_reward
        self.headless = headless
        self.window = None
        if not self.headless:
            _require_pyglet("Interactive rendering")
        self.shape_factory = ShapeFactory(use_pyglet=not self.headless)
        if not self.headless:
            self.window = Window(
                width=WINDOW_WIDTH, height=WINDOW_HEIGHT, visible=False, vsync=False
            )
            glClearColor(0.6667, 0.6471, 1, 1)
            # Ensure vsync is disabled (defensive)
            try:
                self.window.set_vsync(False)
            except Exception:
                pass
        self.level: BaseLevel = LEVELS[level]()
        self.level.attach_factory(self.shape_factory)
        self.random_start = random_start
        self.eliminated = False
        self.max_steps = max_steps
        # Precompute step penalty to avoid per-step division
        self._step_penalty = (
            -0.001 if self.constant_penalty else (-1.0 / self.max_steps)
        )
        # Distance tracking for dense rewards
        self._max_diag = float((WINDOW_WIDTH**2 + WINDOW_HEIGHT**2) ** 0.5)
        self.setup_level_and_player(random_start=self.random_start)

    def setup_rendering(self):
        if self.headless:
            raise RuntimeError("Rendering is disabled while headless=True.")
        _require_pyglet("Window rendering")
        # Re-create the window if it doesn't exist
        if self.window is None:
            self.window = Window(
                width=WINDOW_WIDTH, height=WINDOW_HEIGHT, visible=False, vsync=False
            )
            glClearColor(0.6667, 0.6471, 1, 1)
            try:
                self.window.set_vsync(False)
            except Exception:
                pass
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
        _require_pyglet("Keyboard input handling")
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
        # Cache previous normalized distance for dense reward shaping
        prev_dist_norm = self.prev_dist_norm if self.dense_reward else None
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
            # Avoid printing in training loops for performance
            # print("You lose!")
            self.eliminated = True

        self.level.update()

        # Check if player is completely inside the finish area
        reward, finished = self.player_in_finish_area(interval)
        if collision == 2:
            reward = -1
            finished = True
        else:
            if not finished:
                if self.dense_reward:
                    # Dense reward: negative normalized distance to goal
                    current_dist_norm = self._normalized_distance_to_goal()
                    reward = -current_dist_norm
                    self.prev_dist_norm = current_dist_norm
                else:
                    reward = self._step_penalty
        self.reward = reward
        self.finished = finished

        # Debug plotting hooks (kept for reference)
        # import matplotlib.pyplot as plt
        # plt.imshow(self.get_window_image(), cmap="gray"); plt.show()

        # In headless (training) mode, let the gym env call reset() explicitly.
        # Keep auto-reset for interactive play when a window is visible.
        if not self.headless and (finished or self.eliminated):
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
            self.level.player_start[0],
            self.level.player_start[1],
            self.level.batch,
            self.shape_factory,
        )
        if self.window:
            self.setup_key_handler()
        # Initialize distance tracker when level/player are ready
        self.prev_dist_norm = self._normalized_distance_to_goal()

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

        # Check collision with each wall line, but first perform fast AABB culling
        p_left = player_rect["left"]
        p_right = player_rect["right"]
        p_bottom = player_rect["bottom"]
        p_top = player_rect["top"]
        for line in self.level.wall_lines:
            # Line segment AABB
            lx1, lx2 = (line.x, line.x2) if line.x <= line.x2 else (line.x2, line.x)
            ly1, ly2 = (line.y, line.y2) if line.y <= line.y2 else (line.y2, line.y)
            # Quick reject if AABBs don't overlap
            if lx2 < p_left or lx1 > p_right or ly2 < p_bottom or ly1 > p_top:
                continue
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

    def _normalized_distance_to_goal(self) -> float:
        """Euclidean distance from player center to the closest point of the finish area,
        normalized by the window diagonal, so it's in [0, ~1]. Inside goal => 0.
        """
        # Player center
        pcx = self.player.object.x + self.player.object.width / 2.0
        pcy = self.player.object.y + self.player.object.height / 2.0
        # Finish rect bounds
        fx1 = self.level.finish_area.x
        fy1 = self.level.finish_area.y
        fx2 = fx1 + self.level.finish_area.width
        fy2 = fy1 + self.level.finish_area.height
        # Closest point on finish rect to player center (clamp)
        cx = min(max(pcx, fx1), fx2)
        cy = min(max(pcy, fy1), fy2)
        dx = pcx - cx
        dy = pcy - cy
        dist = (dx * dx + dy * dy) ** 0.5
        return float(dist / self._max_diag) if self._max_diag > 0 else 0.0

    def get_window_image(self, resize_shape=None) -> np.ndarray:
        if self.headless:
            raise RuntimeError(
                "RGB capture is not available in headless mode. Instantiate the "
                "environment with headless=False or render_mode='human'."
            )
        _require_pyglet("rgb_array capture")
        try:
            # Make sure we're using the correct context
            if not hasattr(self, "_gl_context"):
                # Create a new window and context if needed
                self.window = Window(
                    width=WINDOW_WIDTH, height=WINDOW_HEIGHT, visible=False, vsync=False
                )
                self._gl_context = self.window.context
                glClearColor(0.6667, 0.6471, 1, 1)
                try:
                    self.window.set_vsync(False)
                except Exception:
                    pass

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
