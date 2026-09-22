"""Public shape contract, with no learned policy or robot driver implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence
import math


@dataclass(frozen=True)
class ActionSpec:
    embodiment: str
    dimension: int
    latent_dimension: int | None
    horizon: int = 8
    context_frames: int = 5
    image_height: int = 64
    image_width: int = 64

    def validate_chunk(self, chunk: Sequence[Sequence[float]]) -> None:
        if len(chunk) != self.horizon:
            raise ValueError(f"Expected {self.horizon} actions, got {len(chunk)}")
        for action in chunk:
            if len(action) != self.dimension:
                raise ValueError(f"Expected {self.dimension} coordinates per action")
            if not all(math.isfinite(float(value)) for value in action):
                raise ValueError("Action coordinates must be finite")


SPECS = {
    "libero": ActionSpec("libero", 7, None),
    "rlbench": ActionSpec("rlbench", 7, 16),
    "arx5": ActionSpec("arx5", 7, 16),
    "so_arm101": ActionSpec("so_arm101", 12, 16),
}


class Policy(Protocol):
    """An interface for separately supplied policy implementations.

    RLBench's seven coordinates are the decoded intermediate representation;
    conversion to the environment's position/quaternion/gripper command is
    outside this interface. No executable model is shipped in this package.
    """

    def predict(self, observation: object, instruction: str) -> Sequence[Sequence[float]]:
        """Return one H-by-action_dimension chunk for the configured embodiment."""
        ...
