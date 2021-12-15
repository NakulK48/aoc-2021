from pathlib import Path
from queue import PriorityQueue
from typing import List

def get_new_cell(cell: int, iteration: int):
    base = cell + iteration
    if base > 9:
        return base - 9
    return base

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
        base_raw_grid = []
        for line in raw.split("\n"):
            base_line = [int(c) for c in line]
            result_line = []
            for iteration in range(5):
                result_line += [get_new_cell(cell, iteration) for cell in base_line]
            base_raw_grid.append(result_line)
        raw_grid = []
        for iteration in range(5):
            for line in base_raw_grid:
                new_line = [get_new_cell(cell, iteration) for cell in line]
                raw_grid.append(new_line)
        return Grid(raw_grid)


    @staticmethod
    def distance_grid(basis: "Grid") -> "Grid":
        raw_grid = [
            [float("inf") for _ in range(basis.width)]
            for __ in range(basis.height)
        ]
        raw_grid[0][0] = 0
        return Grid(raw_grid)

    def get(self, x, y):
        return self.grid[x][y]

    def set_if_lower(self, new_value, x, y):
        old_value = self.grid[x][y]
        self.grid[x][y] = min(old_value, new_value)
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
    queue = PriorityQueue()

    queue.put((0, (0, 0)))

    while not queue.empty():
        pos_distance, pos = queue.get()
        if pos in visited:
            continue
        neighbours = cavern.neighbours(*pos)
        for neighbour in neighbours:
            new_dist = pos_distance + cavern.get(*neighbour)
            final_dist = distance.set_if_lower(new_dist, *neighbour)
            queue.put((final_dist, neighbour))

        visited.add(pos)

    return distance.bottom_right()

def part_a():
    cavern = load_cavern()
    return get_cavern_result(cavern)


def part_b():
    cavern = load_repeated_cavern()
    return get_cavern_result(cavern)

print(part_a())
print(part_b())
