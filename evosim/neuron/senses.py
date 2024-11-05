import math
import random
from typing import TYPE_CHECKING

from evosim.constants import MAX_STEPS, SENSE_TYPE, CROWD_DISTANCE


if TYPE_CHECKING:
    from evosim.agent import Agent
    from evosim.genome import Gene


class SensoryCommand:
    id: int
    label: str
    # 0 for Sense, 1 for Internal, 2 for Action
    type: int = SENSE_TYPE

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        raise NotImplementedError

    @classmethod
    def random(cls):
        return random.choice(sensory_commands)()

    @classmethod
    def get_class(cls, id: int):
        for cmd in sensory_commands:
            if cmd.id == id % len(sensory_commands):
                return cmd
        raise IndexError(f"Class id {id % len(sensory_commands)} does not exist")


class AgeSensoryCommand(SensoryCommand):
    id = 0
    label = "AGE"

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        return agent.world.step / MAX_STEPS


class RandomSensoryCommand(SensoryCommand):
    id = 1
    label = "RAND"

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        return random.random()


class XWallSensoryCommand(SensoryCommand):
    """East/west world location"""

    id = 2
    label = "XWALL"

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        distance = max(agent.coord.x, agent.world.len - agent.coord.x)
        return distance / agent.world.len


class YWallSensoryCommand(SensoryCommand):
    """North/south world location"""

    id = 3
    label = "YWALL"

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        distance = max(agent.coord.y, agent.world.len - agent.coord.y)
        return distance / agent.world.len


class NearestWallSensoryCommand(SensoryCommand):
    """Nearest wall"""

    id = 4
    label = "WALL"

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        return max(
            XWallSensoryCommand().execute(agent, inputs, activation_threshold),
            YWallSensoryCommand().execute(agent, inputs, activation_threshold),
        )


class CrowdSensoryCommand(SensoryCommand):
    """How crowded the proximity is"""

    id = 5
    label = "CROWD"

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        radius = CROWD_DISTANCE
        count = 0

        for other_agent in agent.world.agents:
            if other_agent is not agent:
                distance = (
                    (other_agent.coord.x - agent.coord.x) ** 2 + (other_agent.coord.y - agent.coord.y) ** 2
                ) ** 0.5
                if distance <= radius:
                    count += 1

        # Approximate the max no of agents that can fit in the radius
        max_possible_agents_in_radius = int(math.pi * radius**2)
        return min(count / max_possible_agents_in_radius, 1)


class PredictorSensoryCommand(SensoryCommand):
    """Can predict if in a kill zone with a small chance"""

    id = 6
    label = "PRED"

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        prediction_accuracy = 0.1

        is_kill_zone = agent.world.kill_fn(agent.world.len, agent.coord)
        prediction = random.random() < prediction_accuracy

        return 1.0 if prediction == is_kill_zone else 0.0


class DistanceToCenterSensoryCommand(SensoryCommand):
    id = 7
    label = "CEN"

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        # Calculate the center coordinates
        center_x = agent.world.len / 2
        center_y = agent.world.len / 2

        # Calculate the distance from the center
        distance = math.sqrt((agent.coord.x - center_x) ** 2 + (agent.coord.y - center_y) ** 2)

        # Normalize the distance based on the maximum possible distance (diagonal of the world)
        max_distance = math.sqrt(2 * (agent.world.len / 2) ** 2)
        return distance / max_distance


sensory_commands = (
    AgeSensoryCommand,
    RandomSensoryCommand,
    XWallSensoryCommand,
    YWallSensoryCommand,
    NearestWallSensoryCommand,
    CrowdSensoryCommand,
    PredictorSensoryCommand,
)
