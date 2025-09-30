# Create a gymnasium environment for the hardest game, that the state space is the screen pixels and the action space is up, down, left, right.


import gymnasium as gym
from gymnasium import spaces
import numpy as np
from pyglet.window import key
import pyglet

from continuous_maze_env.game.game import ContinuousMazeGame


class ContinuousMazeVizEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(
        self,
        render_mode=None,
        level: str = "level_one",
        max_steps=2500,
        random_start: bool = False,
        obs_shape=(96, 96, 3),
        constant_penalty: bool = False,
        dense_reward: bool = False,
    ):
        super().__init__()

        self.obs_shape = obs_shape
        # Persist config for safe re-creation after close()
        self.level = level
        self.max_steps = max_steps
        self.random_start = random_start
        self.constant_penalty = constant_penalty
        self.dense_reward = dense_reward
        self.render_mode = render_mode

        # Create a display for offscreen rendering if needed
        if render_mode == "rgb_array":
            display = pyglet.canvas.get_display()
            screen = display.get_default_screen()
            config = screen.get_best_config()
            self._context = config.create_context(None)
            self._context.set_current()

        self.game = ContinuousMazeGame(
            level=self.level,
            random_start=self.random_start,
            max_steps=self.max_steps,
            constant_penalty=self.constant_penalty,
            headless=(self.render_mode is None),
            dense_reward=self.dense_reward,
        )
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=self.obs_shape,
            dtype=np.uint8,
        )

        self.max_steps = max_steps
        self.current_step = 0
        self.render_mode = render_mode

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        # If env was closed earlier, re-create the game on reset
        if self.game is None:
            self.game = ContinuousMazeGame(
                level=self.level,
                random_start=self.random_start,
                max_steps=self.max_steps,
                constant_penalty=self.constant_penalty,
                headless=(self.render_mode is None),
                dense_reward=self.dense_reward,
            )
        else:
            self.game.reset_game()
        self.current_step = 0

        # if self.render_mode == "human":
        #     self.game.window.set_visible(True)

        observation = self.game.get_window_image(resize_shape=self.obs_shape)
        info = {}
        return observation, info

    def step(self, action):
        horizontal_action = action[0]
        vertical_action = action[1]
        self.game.step(horizontal_action, vertical_action)
        self.current_step += 1

        observation = self.game.get_window_image(resize_shape=self.obs_shape)
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
        # single draw per frame is enough

    def close(self):
        game = getattr(self, "game", None)
        if game is None:
            return
        try:
            window = getattr(game, "window", None)
            if window is not None:
                try:
                    window.close()
                except Exception:
                    pass
        finally:
            self.game = None
