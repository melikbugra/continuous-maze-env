import gymnasium as gym
from stable_baselines3 import SAC
from continuous_maze_env.envs.continuous_maze_env import ContinuousMazeEnv
import numpy as np
import os
import re


def get_latest_sac_model(models_dir):

    files = os.listdir(models_dir)

    sac_files = [f for f in files if re.match(r"sac_model_\d+_steps\.zip", f)]

    sac_files.sort(key=lambda f: int(re.findall(r"\d+", f)[0]), reverse=True)

    return sac_files[0] if sac_files else None


def play():
    env = gym.make(
        "ContinuousMaze-v0", level="level_two", max_steps=1000, random_start=True
    )

    models_dir = "logs"
    latest_ppo_model = get_latest_sac_model(models_dir)

    print(f"Loading model: {latest_ppo_model}")
    model = SAC.load(os.path.join(models_dir, latest_ppo_model))

    obs, _ = env.reset()

    for _ in range(10):
        env.reset()
        done = False
        steps_passed = 0
        score = 0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            score += reward
            env.render()
            steps_passed += 1
            # print(f"Step: {steps_passed}")
        print(f"Score: {score}")
