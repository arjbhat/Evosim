from collections import defaultdict, deque
from typing import TYPE_CHECKING, Optional, Union

from evosim.activation import execute_action, get_sensory_value
from evosim.constants import ACTION_TYPE

# from evosim.activation import execute_action, get_value
from evosim.genome import Gene, Genome
from evosim.neuron.actions import ActionCommand
from evosim.neuron.internal import InternalCommand
from evosim.neuron.senses import SensoryCommand
from evosim.types import Coord, Direction
from evosim.utils import next_coord, random_position

if TYPE_CHECKING:
    from evosim.world import World


class Agent:
    coord: Coord
    world: "World"
    genome: Genome
    activation_threshold: float  # how much the input gene has to return for the gene to activate
    age: int

    def __init__(
        self,
        world: "World",
        genome_connections: int,
        activation_threshold=0.25,
        coord: Optional[Coord] = None,
    ):
        self.world = world
        if coord is not None:
            self.coord = coord
        else:
            self.coord = random_position(world.len)

        self.genome = Genome.random(genome_connections)
        self.activation_threshold = activation_threshold

        self.age = 0

    def set_genome(self, genome: Genome):
        self.genome = genome

    @classmethod
    def from_parent(cls, parent: "Agent", new_genome: Genome):
        new_agent = Agent(
            world=parent.world,
            genome_connections=0,
            activation_threshold=parent.activation_threshold,
        )
        new_agent.genome = new_genome
        new_agent.age = 0
        return new_agent

    def can_move_in_direction(self, direction: Direction):
        if not self.world.is_coord_free(next_coord(self.coord, direction)):
            return False
        if direction == Direction.N:
            return self.coord.y > 0
        elif direction == Direction.S:
            return self.coord.y < self.world.len - 1
        elif direction == Direction.E:
            return self.coord.x < self.world.len - 1
        elif direction == Direction.W:
            return self.coord.x > 0
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def move(self, direction: Direction):
        if self.can_move_in_direction(direction):
            if direction == Direction.N:
                self.coord.y -= 1
            elif direction == Direction.S:
                self.coord.y += 1
            elif direction == Direction.E:
                self.coord.x += 1
            elif direction == Direction.W:
                self.coord.x -= 1

    @staticmethod
    def topological_sort(genome: Genome) -> list[tuple[Union[SensoryCommand, InternalCommand, ActionCommand], "Gene"]]:
        # Create a dictionary to store in-degree of each vertex
        in_degree = defaultdict(int)
        graph = defaultdict(list)

        # Create the graph and calculate in-degree of each node
        for gene in genome:
            graph[gene.source].append(gene)
            in_degree[gene.target] += 1
            in_degree[gene.source] += 0  # Ensure every vertex is in in_degree

        # Queue for vertices with in-degree 0
        queue = deque([v for v in in_degree if in_degree[v] == 0])

        top_order = []

        while queue:
            vertex = queue.popleft()
            top_order.append((vertex, graph[vertex]))  # this is the next node to be processed

            # Decrease the in-degree of neighbors
            for gene in graph[vertex]:
                in_degree[gene.target] -= 1
                if in_degree[gene.target] == 0:
                    queue.append(gene.target)

        # Check if topological sorting is possible or not
        if len(top_order) != len(in_degree):
            return "Cycle detected! Topological sorting not possible."

        return top_order

    def act(self):
        """Process each connection in the genome to determine outputs"""

        # TODO: this currently assumes only sensor->action

        sorted_neurons = self.topological_sort(self.genome)

        pending_inputs = defaultdict(list)

        for neuron, genes in sorted_neurons:
            value = neuron.execute(self, pending_inputs[neuron], self.activation_threshold)
            for gene in genes:
                pending_inputs[gene.target].append((value, gene.scale_weight()))

    def celebrate_birthday(self):
        self.age += 1

    def get_color(self):
        """Get the color depending on the genome"""

        return self.genome.to_hex()
