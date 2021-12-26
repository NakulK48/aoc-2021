from pathlib import Path
from typing import Iterator, List, Tuple

Position = Tuple[int, int]

def empty_row(length: int):
    return [False for _ in range(length)]

def empty_rows(length: int, count: int):
    return [empty_row(length) for _ in range(count)]

def pad_row(row: List[bool], pad_length: int):
    padding = [False] * pad_length
    return padding + row + padding

class Grid:
    def __init__(self, raw: str, mapper: str, padding: int):
        grid = [[c == "#" for c in line] for line in raw.split("\n")]
        for i, row in enumerate(grid):
            grid[i] = pad_row(row, padding)
        width = len(grid[0])
        self.default = False
        self.grid = empty_rows(width, padding) + grid + empty_rows(width, padding)
        self.height = len(self.grid)
        self.width = width
        self.mapper = mapper

    def clone(self):
        return [[None for _ in range(self.width)] for __ in range(self.height)]

    def __iter__(self) -> Iterator[Position]:
        for x in range(self.width):
            for y in range(self.height):
                yield (x, y)

    def get(self, x: int, y: int) -> bool:
        if x >= self.width or y >= self.height:
            return self.default
        if self.grid[y][x] is None:
            raise ValueError()
        return self.grid[y][x]

    def __str__(self):
        result = "  "
        for i in range(self.width):
            result += f"{i}"
        result += "\n"
        for i, row in enumerate(self.grid):
            result += f"{i} "
            for char in row:
                result += ("#" if char else ".")
            result += "\n"
        return result

    def square(self, x: int, y: int) -> List[Position]:
        return [
            (x+xdiff, y+ydiff)
            for ydiff in range(-1, 2)
            for xdiff in range(-1, 2)
        ]

    def count_lit(self) -> int:
        return sum(1 for row in self.grid for cell in row if cell)

    def new_value(self, x: int, y: int):
        input_pixels = self.square(x, y)
        input_bits = [self.get(*pos) for pos in input_pixels]
        input_string = "".join(str(int(n)) for n in input_bits)
        input_index = int(input_string, 2)
        return self.mapper[input_index] == "#"

def load_grid(padding: int):
    raw = Path("problem_20.txt").read_text().strip()
    mapper, raw_image = raw.split("\n\n")
    return Grid(raw_image, mapper.replace("\n", ""), padding)


def run_iterations(iterations: int):
    base_grid = load_grid(iterations)
    grid = base_grid
    for _ in range(iterations):
        total_set = 0
        new_raw_grid = grid.clone()
        for x, y in grid:
            new_value = grid.new_value(x, y)
            total_set += int(new_value)
            new_raw_grid[y][x] = new_value
        grid.grid = new_raw_grid
        grid.default = new_raw_grid[0][0]
    return total_set

def part_a():
    return run_iterations(2)

def part_b():
    return run_iterations(50)

print(part_a())
print(part_b())

