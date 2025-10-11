from time import perf_counter
import statistics as stats
import gymnasium as gym
import numpy as np
import continuous_maze_env

# Simple headless benchmark for the Gym env
# Measures wall-clock for N episodes of M random steps each.


def run_benchmark(level: str = "level_four", episodes: int = 10, steps: int = 1000):
    times = []
    total_steps = 0
    for ep in range(episodes):
        env = gym.make(
            "ContinuousMaze-v0",
            level=level,
            max_steps=steps,
            random_start=True,
            render_mode=None,
        )
        obs, info = env.reset()
        t0 = perf_counter()
        for i in range(steps):
            a = env.action_space.sample()
            obs, r, term, trunc, info = env.step(a)
            total_steps += 1
            if term or trunc:
                break
        t1 = perf_counter() - t0
        times.append(t1)
        env.close()

    mean = stats.mean(times)
    stdev = stats.pstdev(times) if len(times) > 1 else 0.0
    steps_per_sec = (total_steps / sum(times)) if sum(times) > 0 else float("nan")
    print(
        f"Level={level} Episodes={episodes} Steps/Ep={steps}\n"
        f"Episode time mean={mean:.6f}s stdev={stdev:.6f}s\n"
        f"Total steps={total_steps} Aggregate throughput ~{steps_per_sec:.1f} steps/s"
    )


if __name__ == "__main__":
    # Default quick run. Adjust as needed.
    run_benchmark(level="level_four", episodes=5, steps=500)
