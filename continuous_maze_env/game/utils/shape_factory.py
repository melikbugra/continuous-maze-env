"""Rendering backend abstractions for headless-friendly geometry."""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any


class DummyBatch:
    """No-op batch used when pyglet graphics are unavailable."""

    def draw(self) -> None:  # pragma: no cover - noop
        return


@dataclass
class DummyRectangle:
    x: float
    y: float
    width: float
    height: float
    color: Any = None
    batch: Any = None


@dataclass
class DummyCircle:
    x: float
    y: float
    radius: float
    color: Any = None
    batch: Any = None


@dataclass
class DummyLine:
    x: float
    y: float
    x2: float
    y2: float
    width: float = 1.0
    color: Any = None
    batch: Any = None


@dataclass
class DummyBorderedRectangle(DummyRectangle):
    border: float = 0.0
    border_color: Any = None


_DUMMY_SHAPES = SimpleNamespace(
    Rectangle=DummyRectangle,
    Circle=DummyCircle,
    Line=DummyLine,
)


class ShapeFactory:
    """Creates either real pyglet shapes or lightweight headless surrogates."""

    def __init__(self, use_pyglet: bool = True):
        self._backend = "dummy"
        self._batch_cls: type[Any] = DummyBatch
        self.shapes = _DUMMY_SHAPES
        self.BorderedRectangle = DummyBorderedRectangle
        if use_pyglet:
            self._activate_pyglet_backend()

    def _activate_pyglet_backend(self) -> None:
        try:
            from pyglet import shapes as pyglet_shapes
            from pyglet.graphics import Batch as PygletBatch
            from pyglet.shapes import BorderedRectangle as PygletBorderedRectangle
        except Exception as exc:  # pragma: no cover - import guard
            raise RuntimeError(
                "Pyglet rendering backend is not available on this system"
            ) from exc
        self._backend = "pyglet"
        self._batch_cls = PygletBatch
        self.shapes = pyglet_shapes
        self.BorderedRectangle = PygletBorderedRectangle

    def force_dummy_backend(self) -> None:
        self._backend = "dummy"
        self._batch_cls = DummyBatch
        self.shapes = _DUMMY_SHAPES
        self.BorderedRectangle = DummyBorderedRectangle

    def create_batch(self):
        return self._batch_cls()

    @property
    def is_pyglet(self) -> bool:
        return self._backend == "pyglet"
