# Create a gymnasium environment for the hardest game, that the state space is the screen pixels and the action space is up, down, left, right.


import gymnasium as gym
from gymnasium import spaces
import numpy as np
from pyglet.window import key
import pyglet

from continuous_maze_env.game.game import ContinuousMazeGame


class ContinuousMazeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(
        self,
        render_mode=None,
        level: str = "level_one",
        max_steps=2500,
        random_start: bool = False,
        obs_shape=(96, 96, 3),
    ):
        super().__init__()

        self.obs_shape = obs_shape

        # Create a display for offscreen rendering if needed
        if render_mode == "rgb_array":
            display = pyglet.canvas.get_display()
            screen = display.get_default_screen()
            config = screen.get_best_config()
            self._context = config.create_context(None)
            self._context.set_current()

        self.game = ContinuousMazeGame(
            level=level, random_start=random_start, max_steps=max_steps
        )
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        # self.observation_space = spaces.Box(
        #     low=0,
        #     high=255,
        #     shape=self.obs_shape,
        #     dtype=np.uint8,
        # )
        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(2,),
            dtype=np.float32,
        )

        self.max_steps = max_steps
        self.current_step = 0
        self.render_mode = render_mode

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.game.reset_game()
        self.current_step = 0

        # if self.render_mode == "human":
        #     self.game.window.set_visible(True)

        # observation = self.game.get_window_image(resize_shape=self.obs_shape)
        observation = self._get_normalized_observation()
        info = {}
        return observation, info

    def step(self, action):
        horizontal_action = action[0]
        vertical_action = action[1]
        self.game.step(horizontal_action, vertical_action)
        self.current_step += 1

        # observation = self.game.get_window_image(resize_shape=self.obs_shape)
        observation = self._get_normalized_observation()
        reward = self.game.get_reward()
        done = self.game.is_done()

        terminated = done
        truncated = self.current_step >= self.max_steps

        info = {}

        return observation, reward, terminated, truncated, info

    def render(self, mode="human"):
        if self.render_mode == "rgb_array":
            return self.game.get_window_image()  # Full size for rendering
        self.game.setup_rendering()
        self.game.window.switch_to()
        self.game.window.dispatch_events()
        self.game.window.clear()
        if self.game.level and self.game.level.batch:
            self.game.level.batch.draw()
        self.game.window.flip()
        if self.game.level and self.game.level.batch:
            self.game.level.batch.draw()
            pass

    def close(self):
        if self.game.window:
            self.game.window.close()
            self.game = None

    def _get_normalized_observation(self):
        x_normalized = self.game.player.object.x / self.game.window.width
        y_normalized = self.game.player.object.y / self.game.window.height
        return np.array([x_normalized, y_normalized], dtype=np.float32).flatten()
