import copy

from evosim.agent import Agent


def clone_reproduce(agents: list["Agent"]) -> list["Agent"]:
    """Reproduce by making a copy"""

    return [*copy.deepcopy(agents), *copy.deepcopy(agents)]


def mutate_reproduce(agents: list["Agent"]) -> list["Agent"]:
    """Reproduce by making a copy"""

    old_agents = copy.deepcopy(agents)

    copied_agents = copy.deepcopy(agents)
    new_agents = []
    for parent in copied_agents:
        new_genome = parent.genome.to_mutated()

        new_agent = Agent.from_parent(parent, new_genome)
        new_agents.append(new_agent)

    return [*old_agents, *new_agents]
