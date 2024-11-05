import os
import random

from evosim.types import Coord, Direction


def random_position(size) -> Coord:
    """Generate a random position in the world"""

    x = random.randint(0, size - 1)
    y = random.randint(0, size - 1)
    return Coord(x, y)


def random_index(list: list) -> int:
    """Get a random index in the list"""

    return random.randint(0, len(list) - 1)


def is_index_in_list(items: list, index: int) -> bool:
    """Determine if the given index is a valid index for the list"""

    return -len(items) <= index < len(items)


def next_coord(coord: Coord, direction: Direction) -> Coord:
    if direction == Direction.N:
        return Coord(coord.x, coord.y - 1)
    elif direction == Direction.E:
        return Coord(coord.x + 1, coord.y)
    elif direction == Direction.S:
        return Coord(coord.x, coord.y + 1)
    elif direction == Direction.W:
        return Coord(coord.x - 1, coord.y)
    else:
        raise ValueError(f"Invalid direction: {direction}")


def hex_to_rgba(hex_color):
    """Convert a hex color to an RGBA tuple."""
    hex_color = hex_color.lstrip("#")
    # Handle both RGB and RGBA formats
    if len(hex_color) == 6:
        r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        return r, g, b, 255  # Assuming full opacity for RGB
    elif len(hex_color) == 8:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4, 6))


def rgba_to_hex(rgba):
    """Convert an RGBA tuple to a hex color."""
    # Unpack the tuple and convert each value to hex
    return "#{:02x}{:02x}{:02x}{:02x}".format(*rgba)


def average_hex(hex_colors: list[str]) -> str:
    """Calculate the average color from a list of hex colors."""
    if not hex_colors:
        return "#000000ff"  # Default to black if list is empty

    total_red, total_green, total_blue, total_alpha = 0, 0, 0, 0
    for hex_color in hex_colors:
        rgb = hex_to_rgba(hex_color)
        total_red += rgb[0]
        total_green += rgb[1]
        total_blue += rgb[2]
        total_alpha += rgb[3]

    average_red = int(total_red / len(hex_colors))
    average_green = int(total_green / len(hex_colors))
    average_blue = int(total_blue / len(hex_colors))
    average_alpha = int(total_alpha / len(hex_colors))

    return rgba_to_hex((average_red, average_green, average_blue, average_alpha))


def create_dir(path: str):
    """Create dir if not exists"""
    
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except: print(f"{path} exists")
