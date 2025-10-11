from continuous_maze_env.game.game import ContinuousMazeGame
from continuous_maze_env.game.levels.level_one import LevelOne
from continuous_maze_env.game.levels.level_two import LevelTwo
from continuous_maze_env.game.levels.level_three import LevelThree
from continuous_maze_env.game.levels.level_four import LevelFour
from continuous_maze_env.envs.continuous_maze_env import ContinuousMazeEnv
import gymnasium as gym
import continuous_maze_env
from time import sleep


from time import perf_counter


def run_game():
    start_time = perf_counter()
    game = ContinuousMazeGame(level="level_two", random_start=True)
    game.setup_rendering()

    game.run()
    print(f"Time taken: {perf_counter() - start_time}")


def run_env():
    start_time = perf_counter()
    # env = ContinuousMazeEnv(
    #     level="level_four", random_start=True, max_steps=1000, render_mode=None
    # )

    env = gym.make(
        "ContinuousMaze-v0",
        level="level_three",
        max_steps=200,
        random_start=True,
        render_mode=None,
    )

    obs, info = env.reset()
    x = 0
    done = False
    while not done:
        action = env.action_space.sample()
        # sleep(0.02)
        # print(action)
        obs, rew, term, trun, info = env.step(action)
        # env.render()
        x += 1
        # if x > 100:
        #     break
        done = term or trun

        if term:
            print("Goal reached!")
        if trun:
            print("Max steps reached!")

    print(f"Time taken: {perf_counter() - start_time}")


if __name__ == "__main__":
    run_env()
    # run_game()
