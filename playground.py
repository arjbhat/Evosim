from evosim.constants import WORLD_LEN
from evosim.genome import Gene, Genome
from evosim.agent import Agent
from evosim.kill_fn import center_circle_kill_fn, middle_kill_fn, outside_circle_kill_fn, visualize_kill_zone
from evosim.types import Coord, Direction
from evosim.neuron.actions import MoveRandomCommand
from evosim.neuron.senses import AgeSensoryCommand, RandomSensoryCommand


visualize_kill_zone(WORLD_LEN, center_circle_kill_fn, 'center-kill.png')
visualize_kill_zone(WORLD_LEN, middle_kill_fn, 'middle.png')
visualize_kill_zone(WORLD_LEN, outside_circle_kill_fn, 'center-life.png')
