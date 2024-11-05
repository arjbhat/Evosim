import copy
from typing import TYPE_CHECKING, Callable, Optional

from tqdm import tqdm

from evosim.agent import Agent
from evosim.constants import LIFESPAN, MAX_STEPS, NUM_GENERATIONS
from evosim.types import AgentVisInfo, Coord, KillFn, Log, ReproductionFn
from evosim.utils import random_position


class World:
    len: int
    agents: list[Agent]

    generation: int
    step: int

    kill_fn: KillFn
    reproduction_fn: ReproductionFn

    def __init__(
        self,
        len: int,
        initial_population: int,
        genome_connections: int,
        kill_fn: KillFn,
        reproduction_fn: ReproductionFn,
    ):
        self.len = len
        self.agents = [
            Agent(
                world=self,
                genome_connections=genome_connections,
            )
            for _ in range(initial_population)
        ]

        self.step = 0
        self.generation = 0

        self.kill_fn = kill_fn
        self.reproduction_fn = reproduction_fn

        # TODO make sure there are no 2 agents in same coord ?
        self.randomize_agent_coords()

    def provide_agents(self, agents: list["Agent"]):
        self.agents = agents
        self.randomize_agent_coords()

    def is_coord_free(self, coord: Coord):
        for agent in self.agents:
            if agent.coord == coord:
                return False
        return True

    def randomize_agent_coords(self):
        """Scatter the agents"""

        coords = []

        for agent in self.agents:
            while True:
                coord = random_position(self.len)
                if coord not in coords:
                    agent.coord = coord
                    break

    def selectively_kill(self):
        """Only agents a certain distance from the right/left walls will survive"""

        distance = 5
        surviving_agents = []

        for agent in self.agents:
            if self.kill_fn(self.len, agent.coord):
                # Dead
                ...
            else:
                surviving_agents.append(agent)

        self.agents = surviving_agents

    def kill_old_age(self):
        """Kill agents of old age"""

        surviving_agents = []

        for agent in self.agents:
            if agent.age >= LIFESPAN:
                # Dead
                ...
            else:
                surviving_agents.append(agent)

        # print(f"{len(self.agents)-len(surviving_agents)} died of old age lmao")

        self.agents = surviving_agents

    def reproduce_agents(self):
        """Have all the agents reproduce"""

        self.agents = self.reproduction_fn(self.agents)

    def simulate_generation(self, gen: int):
        self.step = 0

        print(f"\nGeneration {gen}")
        print(f"Population: {len(self.agents)}")

        for i in tqdm(range(MAX_STEPS)):
            for agent in self.agents:
                agent.act()

            # Save to log

            self.log.append(
                Log(
                    world_len=self.len,
                    generation=gen,
                    step=i,
                    agents=[
                        AgentVisInfo(coord=copy.deepcopy(agent.coord), color=agent.get_color()) for agent in self.agents
                    ],
                )
            )

        self.selectively_kill()
        self.reproduce_agents()
        for agent in self.agents:
            agent.celebrate_birthday()
        self.randomize_agent_coords()
        self.kill_old_age()

        print(f"Generation {gen} complete.")

    def simulate(self) -> list[Log]:
        print("Starting simulation ...")
        print("Initial genomes:")
        for agent in self.agents:
            print(agent.genome)

        # Reset log
        self.log = []

        for i in range(NUM_GENERATIONS):
            self.simulate_generation(i)
        print("Simulation complete")

        print("Final genomes:")
        for agent in self.agents:
            print(agent.genome)

        return self.log
