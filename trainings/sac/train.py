import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback
from continuous_maze_env.envs.continuous_maze_env import ContinuousMazeEnv
from stable_baselines3.common.noise import NormalActionNoise
import numpy as np

env = gym.make(
    "ContinuousMaze-v0", level="level_one", max_steps=2500, random_start=True
)

# Add exploration noise
n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(
    mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions)
)

# Define the policy network architecture
policy_kwargs = dict(net_arch=[256, 256, 256])

# Create the model with a larger neural network
model = SAC(
    "MlpPolicy",
    env,
    verbose=1,
    device="cuda:0",
    # action_noise=action_noise,
    # policy_kwargs=policy_kwargs,
)

# Create a callback to save the model every 10000 steps
checkpoint_callback = CheckpointCallback(
    save_freq=10000, save_path="./logs/", name_prefix="sac_model"
)

# Train the model
model.learn(total_timesteps=1000000, callback=checkpoint_callback, progress_bar=True)

# Save the model
model.save("sac_continuous_maze")

# To load the model later:
# model = SAC.load("sac_continuous_maze")
