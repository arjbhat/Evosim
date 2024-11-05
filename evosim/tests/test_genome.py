from evosim.genome import Gene, Genome
from evosim.neuron.senses import AgeSensoryCommand, RandomSensoryCommand
from evosim.neuron.actions import MoveEastWestCommand, MoveRandomCommand


def test_genome_str():
    ag_mr = Gene(AgeSensoryCommand(), MoveRandomCommand(), 1)
    assert str(ag_mr) == "AG->MR 1"

    rn_mx = Gene(RandomSensoryCommand(), MoveEastWestCommand(), 21)
    assert str(rn_mx) == "RN->MX 21"

    g = Genome([ag_mr, rn_mx])
    assert str(g) == "[AG->MR 1, RN->MX 21]"
