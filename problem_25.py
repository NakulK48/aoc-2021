import itertools
from pathlib import Path
from copy import deepcopy

class Grid:
    def __init__(self, raw):
        self.grid = [list(line) for line in raw.split("\n")]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def clone(self):
        return [["." for _ in range(self.width)] for __ in range(self.height)]

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y)

    def __str__(self):
        result = ""
        for row in self.grid:
            result += "".join(row)
            result += "\n"
        return result

def load_grid():
    text = Path("problem_25.txt").read_text().strip()
    return Grid(text)

def part_a():
    grid = load_grid()
    for step in itertools.count(start=1):
        new_raw_grid = grid.clone()
        move_occurred = False
        # move right
        for (x, y) in grid:
            current = grid.grid[y][x]
            if current == ".":
                continue
            if current == "v":
                new_raw_grid[y][x] = "v"
                continue
            new_x = x + 1
            if new_x == grid.width:
                new_x = 0
            if grid.grid[y][new_x] == ".":
                new_raw_grid[y][new_x] = ">"
                move_occurred = True
            else:
                new_raw_grid[y][x] = ">"
        grid.grid = deepcopy(new_raw_grid)
        # move down
        for (x, y) in grid:
            current = grid.grid[y][x]
            if current != "v":
                continue
            new_y = y + 1
            if new_y == grid.height:
                new_y = 0
            if grid.grid[new_y][x] == ".":
                new_raw_grid[new_y][x] = "v"
                new_raw_grid[y][x] = "."
                move_occurred = True
            else:
                new_raw_grid[y][x] = "v"
        if not move_occurred:
            break
        grid.grid = new_raw_grid
    return step

print(part_a())