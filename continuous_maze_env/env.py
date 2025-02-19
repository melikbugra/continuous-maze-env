import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pyglet
from continuous_maze_env.game.game import ContinuousMazeGame
from continuous_maze_env.game.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class ContinuousMazeEnv2(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(
        self, level="level_one", max_steps=2500, render_mode=None, random_start=False
    ):
        super().__init__()

        # Set observation dimensions (similar to Atari)
        self.obs_shape = (84, 84, 3)  # Smaller observation space

        # Create a display for offscreen rendering if needed
        if render_mode == "rgb_array":
            display = pyglet.canvas.get_display()
            screen = display.get_default_screen()
            config = screen.get_best_config()
            context = config.create_context(None)
            context.set_current()

        # Initialize the game
        self.game = ContinuousMazeGame(level=level, random_start=random_start)

        # Define action space (continuous actions for x and y movement)
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)

        # Define observation space (RGB image - downscaled)
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=self.obs_shape,
            dtype=np.uint8,
        )

        self.render_mode = render_mode
        if render_mode == "human":
            self.game.setup_rendering()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.game.reset_game()

        if self.render_mode == "human":
            self.game.window.set_visible(True)

        observation = self.game.get_window_image(resize_shape=self.obs_shape)
        info = {}
        return observation, info

    def step(self, action):
        # Take action in the game
        self.game.step(action[0], action[1])

        # Get observation (resized)
        observation = self.game.get_window_image(resize_shape=self.obs_shape)

        # Get reward and done status
        reward = self.game.get_reward()
        terminated = self.game.is_done()
        truncated = False

        info = {}
        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self.game.get_window_image()  # Full size for rendering
        elif self.render_mode == "human":
            self.game.window.set_visible(True)
            return None

    def close(self):
        if self.game.window:
            self.game.window.close()
