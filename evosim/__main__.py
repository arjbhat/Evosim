import random
from typing import TYPE_CHECKING

from evosim.agent import Agent
from evosim.constants import GENOME_CONNECTIONS, INITIAL_POPULATION, MAX_WEIGHT, MIN_WEIGHT, NUM_GENERATIONS, WORLD_LEN
from evosim.genome import Gene, Genome
from evosim.kill_fn import center_circle_kill_fn, middle_kill_fn, outside_circle_kill_fn, visualize_kill_zone
from evosim.neuron.actions import (
    MoveEastWestCommand,
    MoveNorthSouthCommand,
    MoveRandomCommand,
    MoveToCenterCommand,
    MoveToClosestAgentCommand,
)
from evosim.neuron.internal import InternalCommand
from evosim.neuron.senses import (
    AgeSensoryCommand,
    CrowdSensoryCommand,
    DistanceToCenterSensoryCommand,
    RandomSensoryCommand,
    XWallSensoryCommand,
    YWallSensoryCommand,
)
from evosim.reproduce_fn import clone_reproduce, mutate_reproduce
from evosim.types import Log
from evosim.visualize import visualize
from evosim.world import World

kill_fn = outside_circle_kill_fn
reproduce_fn = mutate_reproduce


def main():
    world = World(
        len=WORLD_LEN,
        initial_population=INITIAL_POPULATION,
        genome_connections=GENOME_CONNECTIONS,
        kill_fn=kill_fn,
        reproduction_fn=reproduce_fn,
    )

    visualize_kill_zone(WORLD_LEN, kill_fn, "./current-kill-zone.png")

    # Gene pool:
    # init_agents = []
    # for i in range(200):
    #     agent = Agent(world, 0, activation_threshold=0.9)
    #     dtc = DistanceToCenterSensoryCommand()
    #     agent.set_genome(
    #         Genome(
    #             [
    #                 Gene(RandomSensoryCommand(), MoveNorthSouthCommand(), MAX_WEIGHT),
    #                 Gene(AgeSensoryCommand(), MoveNorthSouthCommand(), MAX_WEIGHT),
    #                 Gene(XWallSensoryCommand(), MoveNorthSouthCommand(), MAX_WEIGHT),
    #                 Gene(YWallSensoryCommand(), MoveNorthSouthCommand(), MAX_WEIGHT),
    #                 # Gene(XWallSensoryCommand(), InternalCommand.get_class(0), MAX_WEIGHT),
    #                 # Gene(YWallSensoryCommand(), InternalCommand.get_class(0), MAX_WEIGHT),
    #                 # Gene(dtc, InternalCommand.get_class(0), MAX_WEIGHT),
    #                 # Gene(dtc, InternalCommand.get_class(1), MAX_WEIGHT),
    #                 # Gene(CrowdSensoryCommand(), InternalCommand.get_class(2), MAX_WEIGHT),
    #                 # Gene(InternalCommand.get_class(0), InternalCommand.get_class(2), MAX_WEIGHT),
    #                 # Gene(InternalCommand.get_class(0), MoveEastWestCommand(), MAX_WEIGHT),
    #                 # Gene(InternalCommand.get_class(1), MoveNorthSouthCommand(), MAX_WEIGHT),
    #                 # Gene(InternalCommand.get_class(2), MoveToClosestAgentCommand(), MAX_WEIGHT),
    #             ]
    #         )
    #     )
    #     init_agents.append(agent)
    # world.provide_agents(init_agents)

    log = world.simulate()

    print("Creating visualizations ...")

    logs_by_gen: list[list["Log"]] = [[] for _ in range(NUM_GENERATIONS)]

    for log_state in log:
        logs_by_gen[log_state.generation].append(log_state)

    visualize(logs_by_gen, kill_fn)

    print("Visualizations complete")


if __name__ == "__main__":
    main()
