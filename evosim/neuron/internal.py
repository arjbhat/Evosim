import random
from typing import TYPE_CHECKING

from evosim.constants import MAX_WEIGHT, NUM_INTERNAL_NEURONS, INTERNAL_TYPE
from evosim.types import Direction

if TYPE_CHECKING:
    from evosim.agent import Agent
    from evosim.genome import Gene


class InternalCommand:
    id: int
    label: str
    # 0 for Sense, 1 for Internal, 2 for Action
    type: int = INTERNAL_TYPE

    def __init__(self, id: int):
        self.id = id
        self.label = f"INTR{id}"

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        return self.apply_scalar(inputs)

    @classmethod
    def generate_instances(cls, num_neurons: int):
        return [cls(i) for i in range(num_neurons)]

    @classmethod
    def random(cls):
        return random.choice(internal_commands)

    @classmethod
    def get_class(cls, id: int):
        for cmd in internal_commands:
            if cmd.id == id % len(internal_commands):
                return cmd
        raise IndexError(f"Class id {id % len(internal_commands)} does not exist")

    @staticmethod
    def apply_scalar(inputs: list[tuple[float, float]]):
        scale_fac = len(inputs) * 4 if len(inputs) != 0 else 1
        return sum(value * weight for value, weight in inputs) / scale_fac


# class InternalCommand(InternalCommand):
#     def execute(self, agent: "Agent", gene: "Gene"):
#         retries = 0
#         while retries <= 5:
#             direction = self.get_direction(agent, gene)
#             if direction and agent.can_move_in_direction(direction):
#                 agent.move(direction)
#                 break
#             retries += 1

#     def get_direction(self, agent: "Agent", gene: "Gene") -> Direction:
#         raise NotImplementedError


internal_commands = InternalCommand.generate_instances(NUM_INTERNAL_NEURONS)
