from continuous_maze_env.game.game import ContinuousMazeGame
from continuous_maze_env.game.levels.level_one import LevelOne
from continuous_maze_env.game.levels.level_two import LevelTwo
from continuous_maze_env.envs.continuous_maze_env import ContinuousMazeEnv


def run_game():
    game = ContinuousMazeGame(level="level_two", random_start=True)
    game.setup_rendering()

    game.run()


def run_env():
    env = ContinuousMazeEnv(level="level_two", random_start=True)
    for _ in range(100):
        obs, info = env.reset()
        x = 0
        while True:
            action = env.action_space.sample()
            # print(action)
            obs, rew, _, _, _ = env.step(action)
            env.render()
            x += 1
            if x > 100:
                break


if __name__ == "__main__":
    run_env()
    # run_game()
