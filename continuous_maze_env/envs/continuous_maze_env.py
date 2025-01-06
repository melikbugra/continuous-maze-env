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
    ):
        super().__init__()
        self.game = ContinuousMazeGame(
            level=level, random_start=random_start, max_steps=max_steps
        )
        self.action_space = spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(1, 2),
            dtype=np.float32,
        )

        self.max_steps = max_steps
        self.current_step = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game.reset_game()
        self.current_step = 0

        observation = self._get_normalized_observation()
        return observation, {}

    def step(self, action):
        horizontal_action = np.cos(action[0] * 2 * np.pi)
        vertical_action = np.sin(action[0] * 2 * np.pi)
        self.game.step(horizontal_action, vertical_action)
        self.current_step += 1

        observation = self._get_normalized_observation()
        reward = self.game.get_reward()
        done = self.game.is_done()

        terminated = done
        truncated = self.current_step >= self.max_steps

        info = {}

        return observation, reward, terminated, truncated, info

    def render(self, mode="human"):
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
        self.game.window.close()
        self.game = None

    def _get_normalized_observation(self):
        x_normalized = self.game.player.object.x / self.game.window.width
        y_normalized = self.game.player.object.y / self.game.window.height
        return np.array([x_normalized, y_normalized], dtype=np.float32).reshape(1, -1)
