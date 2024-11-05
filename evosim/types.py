import random
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from evosim.agent import Agent


@dataclass
class Coord:
    x: int
    y: int


class Direction(Enum):
    N = 1
    E = 2
    S = 3
    W = 4

    @classmethod
    def random(cls):
        return random.choice(list(Direction))


def opposite_direction( direction: "Direction") -> "Direction":
    if direction == Direction.N:
        return Direction.S
    if direction == Direction.E:
        return Direction.W
    if direction == Direction.W:
        return Direction.E
    if direction == Direction.S:
        return Direction.N


@dataclass
class AgentVisInfo:
    """Relevant information from agent required for visualization"""

    coord: Coord
    color: str


@dataclass
class Log:
    world_len: int
    generation: int
    step: int
    agents: list["AgentVisInfo"]  # all contains coordinates


KillFn = Callable[[int, "Coord"], bool]

ReproductionFn = Callable[[list["Agent"]], list["Agent"]]
