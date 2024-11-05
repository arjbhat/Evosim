from evosim.world import World, Agent
from evosim.types import Coord, Direction


def test_moving():
    w = World(
        len=50, initial_population=10, genome_connections=2, kill_fn=lambda x, y: False
    )
    a = Agent(
        world=w,
        coord=Coord(x=0, y=0),
        genome_connections=1,
    )

    assert a.coord == Coord(x=0, y=0)

    assert a.can_move_in_direction(Direction.E)
    assert a.can_move_in_direction(Direction.S)
    assert not a.can_move_in_direction(Direction.W)
    assert not a.can_move_in_direction(Direction.N)

    a.move(Direction.E)
    assert a.coord == Coord(x=1, y=0)

    a.move(Direction.S)
    assert a.coord == Coord(x=1, y=1)

    assert a.can_move_in_direction(Direction.N)
    a.move(Direction.N)
    assert a.coord == Coord(x=1, y=0)

    assert a.can_move_in_direction(Direction.W)
    a.move(Direction.W)
    assert a.coord == Coord(x=0, y=0)


def test_moving_directions():
    w = World(
        len=50, initial_population=2, genome_connections=2, kill_fn=lambda x, y: False
    )
    a, b = w.agents[0], w.agents[1]

    a.coord = Coord(x=0, y=0)
    b.coord = Coord(x=0, y=1)

    assert a.can_move_in_direction(Direction.S) == False
    assert w.is_coord_free(Coord(x=0, y=1)) == False

    assert a.can_move_in_direction(Direction.E)
    a.move(Direction.E)

    assert a.coord == Coord(x=1, y=0)
