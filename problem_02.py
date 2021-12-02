from pathlib import Path
from enum import Enum

class Direction(Enum):
    FORWARD = 1
    UP = 2
    DOWN = 3


def parse_line(line: str):
    raw_direction, raw_dist = line.split()
    return (Direction[raw_direction.upper()], int(raw_dist))

def load_instructions():
    lines = Path("problem_02.txt").read_text().strip().split("\n")
    return [parse_line(line) for line in lines]

def part_a():
    instructions = load_instructions()
    depth = position = 0
    for direction, length in instructions:
        if direction == Direction.FORWARD:
            position += length
        elif direction == Direction.UP:
            depth -= length
        elif direction == Direction.DOWN:
            depth += length
    return (depth * position)


def part_b():
    instructions = load_instructions()
    depth = position = aim = 0
    for direction, length in instructions:
        if direction == Direction.FORWARD:
            position += length
            depth += (aim * length)
        elif direction == Direction.UP:
            aim -= length
        elif direction == Direction.DOWN:
            aim += length
    return (depth * position)

print(part_a())
print(part_b())