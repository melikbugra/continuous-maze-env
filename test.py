import cv2
import numpy as np
from gymnasium import ObservationWrapper
from gymnasium.spaces import Box
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from continuous_maze_env.envs.continuous_maze_env import ContinuousMazeEnv
import gymnasium as gym


class ResizeObservation(ObservationWrapper):
    def __init__(self, env, shape):
        super(ResizeObservation, self).__init__(env)
        self.shape = shape
        self.observation_space = Box(low=0, high=255, shape=self.shape, dtype=np.uint8)

    def observation(self, observation):
        return cv2.resize(observation, self.shape[:2], interpolation=cv2.INTER_AREA)


class NormalizeObservation(ObservationWrapper):
    def __init__(self, env):
        super(NormalizeObservation, self).__init__(env)
        self.observation_space = Box(
            low=0.0, high=1.0, shape=env.observation_space.shape, dtype=np.float32
        )

    def observation(self, observation):
        return observation / 255.0


# # Create the environment and wrap it
# env = make_vec_env(
#     lambda: ResizeObservation(ContinuousMazeEnv(), (84, 84, 3)),
#     n_envs=1,
# )

# # Define the PPO model with normalize_images=False
# model = PPO("CnnPolicy", env, verbose=1, policy_kwargs={"normalize_images": False})

# # Train the model
# model.learn(total_timesteps=100000)

# # Save the trained model
# model.save("ppo_hardest_game")


# evlaute the model

# Load the trained model
model = PPO.load("ppo_hardest_game")

# Evaluate the model
env = make_vec_env(
    lambda: NormalizeObservation(
        ResizeObservation(ContinuousMazeEnv(render_mode="human"), (84, 84, 3))
    ),
    n_envs=1,
)

obs = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = env.step(action)
    env.render(mode="human")
    if dones:
        obs = env.reset()
