from gymnasium.envs.registration import register

register(
    id="ContinuousMaze-v0",
    entry_point="continuous_maze_env.envs:ContinuousMazeEnv",
)

register(
    id="ContinuousMazeViz-v0",
    entry_point="continuous_maze_env.envs:ContinuousMazeVizEnv",
)
