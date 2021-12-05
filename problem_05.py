from ast import literal_eval
from collections import defaultdict
from math import copysign
from pathlib import Path
from typing import List, Tuple

Position = Tuple[int, int]


def load_lines() -> List[Tuple[Position, Position]]:
    text = Path("problem_05.txt").read_text().strip()
    lines = []
    for line in text.split("\n"):
        start_raw, end_raw = line.split(" -> ")
        start = literal_eval(start_raw)
        end = literal_eval(end_raw)
        lines.append((start, end))
    return lines


def part_a():
    lines = load_lines()
    vents_by_pos = defaultdict(int)
    for ((start_x, start_y), (end_x, end_y)) in lines:  
        if start_x == end_x:
            min_y = min(start_y, end_y)
            max_y = max(start_y, end_y) + 1
            new_vents = [(start_x, new_y) for new_y in range(min_y, max_y)]
        elif start_y == end_y:
            min_x = min(start_x, end_x)
            max_x = max(start_x, end_x) + 1
            new_vents = [(new_x, start_y) for new_x in range(min_x, max_x)]
        else:
            continue
        for new_vent in new_vents:
            vents_by_pos[new_vent] += 1

    num_overlaps = sum(1 for count in vents_by_pos.values() if count >= 2)
    return num_overlaps


def _get_change(start_value, end_value):
    if start_value == end_value:
        return 0
    return int(copysign(1, end_value - start_value))


def _get_length(start_x, start_y, end_x, end_y):
    abs_x = abs(end_x - start_x)
    abs_y = abs(end_y - start_y)
    return max(abs_x, abs_y) + 1


def part_b():
    lines = load_lines()
    vents_by_pos = defaultdict(int)
    for ((start_x, start_y), (end_x, end_y)) in lines:  
        length = _get_length(start_x, start_y, end_x, end_y)
        x_change = _get_change(start_x, end_x)
        y_change = _get_change(start_y, end_y)

        new_vents = [
            (
                start_x + (i * x_change),
                start_y + (i * y_change),
            )
            for i in range(length)
        ]

        for new_vent in new_vents:
            vents_by_pos[new_vent] += 1

    num_overlaps = sum(1 for count in vents_by_pos.values() if count >= 2)
    return num_overlaps

print(part_a())
print(part_b())
