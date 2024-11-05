SENSE_TYPE = 0
INTERNAL_TYPE = 1
ACTION_TYPE = 2

MAX_WEIGHT = 32767  # highest weight for a gene
MIN_WEIGHT = -32768  # lowest weight for a gene

NEURON_ID_BIT_LENGTH = 7  # max bit length of a neuron ID

GENOME_CONNECTIONS = 6  # no of genes in every agent's genome
NUM_INTERNAL_NEURONS = 3

SIGMOID_THRESHOLD = 0.5

# World related
NUM_GENERATIONS = 5
MAX_STEPS = 100  # steps per generation

CROWD_DISTANCE = 5

WORLD_LEN = 64  # world side dimension
INITIAL_POPULATION = 100  # no of agents in generation 0

MUTATION_RATE = 0.01  # chance of mutation

LIFESPAN = 3  # in generations
