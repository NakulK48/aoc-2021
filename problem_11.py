from collections import deque
import itertools
from pathlib import Path
from typing import Deque, List, Iterator, Set, Tuple

Position = Tuple[int, int]

class Grid:
    def __init__(self, raw: str):
        self.grid = [[int(c) for c in line] for line in raw.split("\n")]
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.size = self.height * self.width
        self.flashes = 0
    
    def __iter__(self) -> Iterator[Position]:
        for x in range(self.height):
            for y in range(self.width):
                yield (x, y)

    def get(self, x: int, y: int) -> int:
        return self.grid[x][y]

    def increment(self, x: int, y: int):
        self.grid[x][y] += 1

    def zero(self, x: int, y: int):
        self.grid[x][y] = 0

    def neighbours(self, x: int, y: int) -> List[Position]:
        return [
            (x+xdiff, y+ydiff)
            for xdiff in range(-1, 2)
            for ydiff in range(-1, 2)
            if 0 <= x+xdiff < self.height
            and 0 <= y+ydiff < self.width
            and (xdiff, ydiff) != (0, 0)
        ]

    def maybe_flash(self, pos: Position, has_flashed: Set[Position]) -> List[Position]:
        current = self.get(*pos)
        if current <= 9 or pos in has_flashed:
            return []
        has_flashed.add(pos)
        self.flashes += 1
        return self.neighbours(*pos)

    def iterate_and_count_flashes(self) -> int:
        has_flashed: Set[Position] = set()
        hit_by_flash: Deque[Position] = deque()
        for pos in self:
            self.increment(*pos)
            hit_by_flash += self.maybe_flash(pos, has_flashed)
        while hit_by_flash:
            pos = hit_by_flash.popleft()
            self.increment(*pos)
            hit_by_flash += self.maybe_flash(pos, has_flashed)
        for pos in has_flashed:
            self.zero(*pos)
        return len(has_flashed)


def load_grid() -> Grid:
    text = Path("problem_11.txt").read_text().strip()
    return Grid(text)

def part_a() -> int:
    grid = load_grid()
    for _ in range(100):
        grid.iterate_and_count_flashes()
    return grid.flashes

def part_b() -> int:
    grid = load_grid()
    for step in itertools.count(start=1):
        if grid.iterate_and_count_flashes() == grid.size:
            break
    return step


print(part_a())
print(part_b())
