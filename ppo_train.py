import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback
from continuous_maze_env.envs.continuous_maze_env import ContinuousMazeEnv
from stable_baselines3.common.noise import NormalActionNoise
import numpy as np


env = gym.make("ContinuousMaze-v0", max_steps=5000)

n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(
    mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions)
)

policy_kwargs = dict(net_arch=[256, 256])

model = PPO(
    "CnnPolicy",
    env,
    verbose=1,
    device="cuda:0",
    # action_noise=action_noise,
    # policy_kwargs=policy_kwargs,
)

checkpoint_callback = CheckpointCallback(
    save_freq=10000, save_path="./logs/", name_prefix="ppo_model"
)

model.learn(total_timesteps=1000000, callback=checkpoint_callback, progress_bar=True)

model.save("ppo_continuous_maze")
