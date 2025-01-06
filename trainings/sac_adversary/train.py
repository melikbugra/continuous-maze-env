import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.common.buffers import ReplayBuffer
import continuous_maze_env
from stable_baselines3.common.logger import configure
import torch


def get_adversary_reward(state, protagonist: SAC):
    """
    Returns a scalar adversarial reward based on the difference Q(s,a) - alpha * log pi(a|s).
    Assumes protagonist.policy.actor(state) returns mean and log_std (or something similar)
    from which we create a PyTorch Normal distribution.
    """
    state_tensor = torch.tensor(
        state, dtype=torch.float32, device=protagonist.device
    ).unsqueeze(0)

    sampled_q_values = []
    with torch.no_grad():
        for _ in range(10):
            # Sample an action from the policy (stochastic, as in SAC)
            action = protagonist.policy(state_tensor, deterministic=False)

            q1, q2 = protagonist.critic(state_tensor, action)

            # SAC typically uses the minimum of the two critics
            q_min = torch.min(q1, q2)

            sampled_q_values.append(q_min)

    # Stack and average the Q-values to get the approximate V(s)
    v_est = torch.mean(torch.stack(sampled_q_values), dim=0)
    return v_est.cpu().item()


def train():
    MAX_STEPS = 1000
    Ka = 10
    Kp = 10
    N = 100
    Ha = MAX_STEPS // 2
    Hp = MAX_STEPS // 2

    env = gym.make(
        "ContinuousMaze-v0", level="level_two", max_steps=MAX_STEPS, random_start=True
    )

    adversary = SAC("MlpPolicy", env, verbose=1, device="cuda:0", learning_rate=3e-4)
    adversary_buffer = ReplayBuffer(
        int(1e5), env.observation_space, env.action_space, device=adversary.device
    )
    adversary.replay_buffer = adversary_buffer
    adversary_logger = configure(
        "./logs/",
        ["tensorboard"],
    )
    adversary.set_logger(adversary_logger)

    protagonist = SAC("MlpPolicy", env, verbose=1, device="cuda:0", learning_rate=3e-4)
    protagonist_buffer = ReplayBuffer(
        int(1e5), env.observation_space, env.action_space, device=protagonist.device
    )
    protagonist.replay_buffer = protagonist_buffer
    protagonist_logger = configure(
        "./logs/",
        ["tensorboard"],
    )
    protagonist.set_logger(protagonist_logger)

    for i in range(N):
        print(f"Training iteration {i}")
        scores = []
        for x in range(Ka):
            obs, _ = env.reset()

            # print("Adversary plays...")
            for j in range(Ha):
                if i % 10 == 0 and x == 0:
                    # env.render()
                    pass
                action, _ = adversary.predict(obs, deterministic=False)
                next_obs, _, terminated, truncated, _ = env.step(action)
                reward = get_adversary_reward(next_obs, protagonist)
                adversary.logger.record("adversary/reward", reward)
                adversary.logger.dump(step=i * 100 + x * 10 + j)
                done = terminated or truncated

                adversary.replay_buffer.add(
                    obs,
                    next_obs,
                    action,
                    reward,
                    done,
                    [{"TimeLimit.truncated": False}],
                )
                obs = next_obs
                if terminated:
                    # i = 0
                    obs, _ = env.reset()
                    # print(f"Random adversary terminated episode at step {i}, restarting...")
            adversary.train(gradient_steps=1, batch_size=256)

            # print("Protagonist plays...")
            score = 0
            for k in range(Hp):
                if i % 10 == 0 and k == 0:
                    # env.render()
                    pass
                action, _ = protagonist.predict(obs, deterministic=True)
                next_obs, reward, terminated, truncated, _ = env.step(action)
                score += reward
                done = terminated or truncated
                protagonist.replay_buffer.add(
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
            scores.append(score)

        # print(f"Training iteration {i}, Kp loop")
        for y in range(Kp):
            obs, _ = env.reset()
            # # # print("Adversary plays...")
            for l in range(Ha):
                if i % 10 == 0 and y == 0:
                    # env.render()
                    pass
                action, _ = adversary.predict(obs, deterministic=True)
                next_obs, _, terminated, truncated, _ = env.step(action)
                reward = get_adversary_reward(next_obs, protagonist)

                done = terminated or truncated

                adversary.replay_buffer.add(
                    obs,
                    next_obs,
                    action,
                    reward,
                    done,
                    [{"TimeLimit.truncated": False}],
                )

                if terminated:
                    # i = 0
                    obs, _ = env.reset()
                    # print(f"Random adversary terminated episode at step {i}, restarting...")

            # # # print("Protagonist plays...")
            score = 0
            for m in range(Hp):
                if i % 10 == 0 and m == 0:
                    # env.render()
                    pass
                action, _ = protagonist.predict(obs, deterministic=False)
                next_obs, reward, terminated, truncated, _ = env.step(action)
                protagonist.logger.record("protagonist/reward", reward)
                protagonist.logger.dump(step=i * 100 + y * 10 + m)
                score += reward
                done = terminated or truncated
                protagonist.replay_buffer.add(
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

            protagonist.train(gradient_steps=1, batch_size=256)
            scores.append(score)
        print(f"\n\tMean score: {sum(scores) / len(scores)}")

        protagonist.logger.dump(step=i)
    adversary.save("trainings/sac_adversary/adversary")
    protagonist.save("trainings/sac_adversary/protagonist")
