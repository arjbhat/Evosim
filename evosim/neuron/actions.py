import math
import random
from typing import TYPE_CHECKING

from evosim.constants import MAX_WEIGHT, ACTION_TYPE, SIGMOID_THRESHOLD, WORLD_LEN
from evosim.types import Direction, opposite_direction

if TYPE_CHECKING:
    from evosim.agent import Agent
    from evosim.genome import Gene


class ActionCommand:
    id: int
    label: str
    # 0 for Sense, 1 for Internal, 2 for Action
    type: int = ACTION_TYPE

    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        raise NotImplementedError

    @classmethod
    def random(cls):
        return random.choice(action_outputs)()

    @classmethod
    def get_class(cls, id: int):
        for cmd in action_outputs:
            if cmd.id == id % len(action_outputs):
                return cmd
        raise IndexError(f"Class id {id % len(action_outputs)} does not exist")

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def apply_sigmoid(inputs: list[tuple[float, float]]):
        return ActionCommand.sigmoid(sum(value * weight for value, weight in inputs))


class BaseMoveCommand(ActionCommand):
    def execute(
        self,
        agent: "Agent",
        inputs: list[tuple[float, float]],
        activation_threshold: float,
    ):
        sigmoid = self.apply_sigmoid(inputs)
        if sigmoid < SIGMOID_THRESHOLD + activation_threshold and sigmoid > SIGMOID_THRESHOLD - activation_threshold:
            return
        retries = 0

        while retries <= 5:
            direction = self.get_direction(agent, sigmoid)
            if direction and agent.can_move_in_direction(direction):
                agent.move(direction)
                break
            retries += 1

    def get_direction(self, agent: "Agent", sigmoid: float) -> Direction:
        raise NotImplementedError


class MoveRandomCommand(BaseMoveCommand):
    id = 0
    label = "RAND"

    def get_direction(self, agent: "Agent", sigmoid: float):
        return Direction.random()


class MoveEastWestCommand(BaseMoveCommand):
    id = 1
    label = "X"

    def get_direction(self, agent: "Agent", sigmoid: float):
        return Direction.E if sigmoid < SIGMOID_THRESHOLD else Direction.W


class MoveNorthSouthCommand(BaseMoveCommand):
    id = 2
    label = "Y"

    def get_direction(self, agent: "Agent", sigmoid: float):
        return Direction.N if sigmoid < SIGMOID_THRESHOLD else Direction.S


class MoveToCenterCommand(BaseMoveCommand):
    id = 3
    label = "CENTER"

    def get_direction(self, agent: "Agent", sigmoid: float):
        center_x, center_y = WORLD_LEN // 2, WORLD_LEN // 2

        delta_x = center_x - agent.coord.x
        delta_y = center_y - agent.coord.y

        dir: Direction

        if abs(delta_x) > abs(delta_y):
            if delta_x > 0:
                dir = Direction.E
            else:
                dir = Direction.W
        else:
            if delta_y > 0:
                dir = Direction.S
            else:
                dir = Direction.N

        return dir if sigmoid > SIGMOID_THRESHOLD else opposite_direction(dir)


class MoveToClosestAgentCommand(BaseMoveCommand):
    id = 4
    label = "CLOSE"

    def get_direction(self, agent: "Agent", sigmoid: float):
        closest_agent = self.find_closest_agent(agent)
        if not closest_agent:
            return None

        agent_x, agent_y = agent.coord.x, agent.coord.y
        closest_agent_x, closest_agent_y = closest_agent.coord.x, closest_agent.coord.y

        delta_x = closest_agent_x - agent_x
        delta_y = closest_agent_y - agent_y

        # Determine the primary direction to move towards the closest agent
        if abs(delta_x) > abs(delta_y):
            return Direction.E if delta_x > 0 else Direction.W
        else:
            return Direction.N if delta_y > 0 else Direction.S

    def find_closest_agent(self, agent: "Agent"):
        # Assuming there's a method to get all agents in the environment
        agents = agent.world.agents
        min_distance = float("inf")
        closest_agent = None

        for other_agent in agents:
            if other_agent is agent:
                continue  # Skip the current agent
            distance = self.calculate_distance(agent.coord, other_agent.coord)
            if distance < min_distance:
                min_distance = distance
                closest_agent = other_agent

        return closest_agent

    @staticmethod
    def calculate_distance(coord1, coord2):
        return math.sqrt((coord1.x - coord2.x) ** 2 + (coord1.y - coord2.y) ** 2)


action_outputs = (
    MoveRandomCommand,
    MoveEastWestCommand,
    MoveNorthSouthCommand,
    MoveToCenterCommand,
    MoveToClosestAgentCommand,
)
