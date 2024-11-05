from typing import TYPE_CHECKING

from evosim.neuron.actions import ActionCommand
from evosim.neuron.senses import SensoryCommand

if TYPE_CHECKING:
    from evosim.genome import Gene
    from evosim.world import Agent


def get_sensory_value(sensor: SensoryCommand, agent: "Agent", genes: list["Gene"]):
    return sensor.execute(agent, genes)


def execute_neuron(sensor: SensoryCommand, agent: "Agent", genes: list["Gene"]):
    pass


def execute_action(action: ActionCommand, agent: "Agent", genes: list["Gene"]):
    return action.execute(agent, genes)
