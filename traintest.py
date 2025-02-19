import gymnasium as gym
from stable_baselines3 import SAC, DQN
from stable_baselines3.common.buffers import ReplayBuffer
import continuous_maze_env
from stable_baselines3.common.logger import configure
import torch


iters = 1000
episodes = 10


env = gym.make("CartPole-v1")

model = DQN("MlpPolicy", env, verbose=1, device="cpu", learning_rate=3e-4)
model_buffer = ReplayBuffer(
    int(1e5), env.observation_space, env.action_space, device=model.device
)
model.replay_buffer = model_buffer
model_logger = configure(
    "./logs/",
    ["tensorboard"],
)
model.set_logger(model_logger)

for i in range(iters):
    print(f"Training iteration {i}")
    scores = []
    for x in range(episodes):
        score = 0
        obs, _ = env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=False)
            next_obs, reward, terminated, truncated, _ = env.step(action)
            score += reward
            done = terminated or truncated
            model.replay_buffer.add(
                obs,
                next_obs,
                action,
                reward,
                done,
                [{"TimeLimit.truncated": False}],
            )
            obs = next_obs

        model.train(gradient_steps=2, batch_size=256)
        scores.append(score)

    if i % 100 == 0:
        model.save(f"sac_model_{i}.zip")
    print(f"Average score for iteration {i}: {sum(scores) / len(scores)}")
