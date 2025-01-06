import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.common.buffers import ReplayBuffer
import continuous_maze_env
from stable_baselines3.common.logger import configure


def train():
    MAX_STEPS = 2500
    Ka = 10
    Kp = 10
    N = 100
    Ha = MAX_STEPS // 2
    Hp = MAX_STEPS // 2
    env = gym.make(
        "ContinuousMaze-v0", level="level_two", max_steps=MAX_STEPS, random_start=True
    )
    model = SAC("MlpPolicy", env, verbose=1, device="cuda:0")

    buffer = ReplayBuffer(
        int(1e5), env.observation_space, env.action_space, device=model.device
    )
    model.replay_buffer = buffer

    new_logger = configure(
        "./logs/",
        [
            "stdout",
            #    "csv",
            #    "tensorboard"
        ],
    )
    model.set_logger(new_logger)

    for i in range(N):
        for _ in range(Kp):
            obs, _ = env.reset()
            print("Adversary plays...")
            for i in range(Ha):
                env.render()
                action = env.action_space.sample()
                obs, reward, terminated, truncated, _ = env.step(action)
                done = terminated or truncated
                if done:
                    # i = 0
                    obs, _ = env.reset()
                    # print(f"Random adversary terminated episode at step {i}, restarting...")

            print("Protagonist plays...")
            for i in range(Hp):
                env.render()
                action, _ = model.predict(obs, deterministic=True)
                next_obs, reward, terminated, truncated, _ = env.step(action)
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
                if done:
                    break

            model.train(gradient_steps=1, batch_size=256)

    model.save("random_adversary")
