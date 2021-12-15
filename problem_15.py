import heapq
import math
import time

from pathlib import Path
from typing import List

def get_new_cell(cell: int, iteration: int):
    base = cell + iteration
    if base > 9:
        return base - 9
    return base

def build_2d_array(width: int, height: int, elem: int = 0):
    return [[elem for _ in range(width)] for __ in range(height)]


class Grid:
    def __init__(self, raw_grid: List[List[int]]):
        self.grid = raw_grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    @staticmethod
    def from_string(raw: str) -> "Grid":
        raw_grid = [[int(c) for c in line] for line in raw.split("\n")]
        return Grid(raw_grid)

    @staticmethod
    def from_repeated_string(raw: str) -> "Grid":
        base = Grid.from_string(raw)
        width, height = base.width, base.height
        raw_grid = build_2d_array(width * 5, height * 5)
        for x, row in enumerate(raw_grid):
            for y in range(len(row)):
                raw_grid[x][y] = get_new_cell(
                    cell=base.get_modulo(x, y),
                    iteration=(x // width) + (y // height)
                )
        return Grid(raw_grid)

    @staticmethod
    def distance_grid(basis: "Grid") -> "Grid":
        raw_grid = build_2d_array(basis.width, basis.height, math.inf)
        raw_grid[0][0] = 0
        return Grid(raw_grid)

    def get(self, x, y):
        return self.grid[x][y]

    def get_modulo(self, x, y):
        return self.grid[x % self.width][y % self.height]

    def set_if_lower(self, new_value, x, y):
        self.grid[x][y] = min(self.grid[x][y], new_value)
        return self.grid[x][y]

    def neighbours(self, x, y):
        adjacent = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return [
            (x2, y2) for (x2, y2) in adjacent
            if 0 <= x2 < self.height
            and 0 <= y2 < self.width
        ]
    
    def bottom_right(self):
        return self.grid[-1][-1]

def load_cavern() -> Grid:
    text = Path("problem_15.txt").read_text().strip()
    return Grid.from_string(text)

def load_repeated_cavern() -> Grid:
    text = Path("problem_15.txt").read_text().strip()
    return Grid.from_repeated_string(text)

def get_cavern_result(cavern: Grid):
    distance = Grid.distance_grid(cavern)
    visited = set()
    queue = [(0, (0, 0))]

    while queue:
        pos_distance, pos = heapq.heappop(queue)
        if pos in visited:
            continue
        for neighbour in cavern.neighbours(*pos):
            new_dist = pos_distance + cavern.get(*neighbour)
            final_dist = distance.set_if_lower(new_dist, *neighbour)
            heapq.heappush(queue, (final_dist, neighbour))

        visited.add(pos)

    return distance.bottom_right()

def part_a():
    cavern = load_cavern()
    return get_cavern_result(cavern)


def part_b():
    cavern = load_repeated_cavern()
    return get_cavern_result(cavern)

start = time.time()
print(part_a())
print(part_b())
print(f"Ran in {time.time() - start}s")
