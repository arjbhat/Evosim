from matplotlib import patches, pyplot as plt
from evosim.types import Coord, KillFn


def visualize_kill_zone(world_len, kill_fn: KillFn, outputpath: str):
    fig = plt.figure(figsize=(16, 16))
    plot = fig.add_subplot()
    plt.axis("off")
    # plot.set_title(f"World ({world_len} x {world_len})")
    plot.set_xlim(0, world_len)
    plot.set_ylim(0, world_len)

    all_coords = [Coord(x, y) for x in range(world_len) for y in range(world_len)]
    for coord in all_coords:
        if kill_fn(world_len, coord):
            plot.add_patch(
                patches.Rectangle((coord.x, coord.y), 1, 1, linewidth=0, edgecolor="r", facecolor="red", alpha=0.15)
            )
        else:
            plot.add_patch(
                patches.Rectangle((coord.x, coord.y), 1, 1, linewidth=0, edgecolor="r", facecolor="green", alpha=0.25)
            )

    fig.savefig(outputpath)


def middle_kill_fn(world_len: int, coord: Coord) -> bool:
    """Two strips on either side where the agents live"""

    wall_distance_threshold = world_len // 5
    return not (coord.x < wall_distance_threshold or world_len - wall_distance_threshold <= coord.x)


def center_circle_kill_fn(world_len: int, coord: Coord) -> bool:
    """A circle in the center where agents DIE"""

    center_x = world_len // 2
    center_y = center_x
    radius = world_len // 4

    distance_from_center = ((coord.x - center_x) ** 2 + (coord.y - center_y) ** 2) ** 0.5

    return distance_from_center <= radius


def outside_circle_kill_fn(world_len: int, coord: Coord) -> bool:
    """A circle in the center where agents LIVE"""

    return not center_circle_kill_fn(world_len, coord)
