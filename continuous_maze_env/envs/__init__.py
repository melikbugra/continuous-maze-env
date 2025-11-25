from __future__ import annotations

from typing import TYPE_CHECKING, Any

from continuous_maze_env.envs.continuous_maze_env import ContinuousMazeEnv

__all__ = ["ContinuousMazeEnv", "ContinuousMazeVizEnv"]

if TYPE_CHECKING:  # pragma: no cover - only for static analyzers
    from continuous_maze_env.envs.continuous_maze_viz_env import ContinuousMazeVizEnv


def __getattr__(name: str) -> Any:
    if name == "ContinuousMazeVizEnv":
        from continuous_maze_env.envs.continuous_maze_viz_env import (
            ContinuousMazeVizEnv as _VizEnv,
        )

        return _VizEnv
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
