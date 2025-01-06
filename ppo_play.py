import gymnasium as gym
from stable_baselines3 import PPO
from continuous_maze_env.envs.continuous_maze_env import ContinuousMazeEnv
import numpy as np
import os
import re


def get_latest_ppo_model(models_dir):

    files = os.listdir(models_dir)

    ppo_files = [f for f in files if re.match(r"ppo_model_\d+_steps\.zip", f)]

    ppo_files.sort(key=lambda f: int(re.findall(r"\d+", f)[0]), reverse=True)

    return ppo_files[0] if ppo_files else None


env = gym.make("ContinuousMaze-v0", max_steps=5000)

models_dir = "logs"
latest_ppo_model = get_latest_ppo_model(models_dir)

print(f"Loading model: {latest_ppo_model}")
model = PPO.load(os.path.join(models_dir, latest_ppo_model))

obs, _ = env.reset()


for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    print(action)
    obs, reward, done, truncated, info = env.step(action)
    env.render()
    if done or truncated:
        obs, _ = env.reset()

env.close()
