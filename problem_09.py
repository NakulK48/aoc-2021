from collections import defaultdict, deque
from pathlib import Path

KNOWN_BOTTOMS = {}

class Grid:
    def __init__(self, raw):
        self.grid = [[int(c) for c in line] for line in raw.split("\n")]
        self.height = len(self.grid)
        self.width = len(self.grid[0])
    
    def get(self, x, y):
        return self.grid[x][y]

    def neighbours(self, x, y):
        adjacent = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return [
            (x2, y2) for (x2, y2) in adjacent
            if 0 <= x2 < self.height
            and 0 <= y2 < self.width
        ]

    def is_lowest(self, x, y):
        current = self.get(x, y)
        return all(self.get(*pos) > current for pos in self.neighbours(x, y))

    def get_basin_bottom(self, x, y):
        if self.get(x, y) == 9:
            return None
        cands = deque([(x, y)])
        explored = set()
        while cands:
            cand = cands.popleft()
            if cand in KNOWN_BOTTOMS:
                return KNOWN_BOTTOMS[cand]
            current = self.get(*cand)
            if self.is_lowest(*cand):
                for old_pos in explored:
                    KNOWN_BOTTOMS[old_pos] = cand
                return cand
            lower_neighbours = [
                pos for pos in self.neighbours(*cand)
                if pos not in explored
                and self.get(*pos) < current
            ]
            cands += lower_neighbours
            explored.add(cand)

    def __iter__(self):
        for x in range(self.height):
            for y in range(self.width):
                yield (x, y)


def load_grid():
    text = Path("problem_09.txt").read_text().strip()
    return Grid(text)

def part_a():
    grid = load_grid()
    total_risk = 0
    for (x, y) in grid:
        if grid.is_lowest(x, y):
            total_risk += grid.get(x, y) + 1
    return total_risk


def part_b():
    grid = load_grid()
    positions_by_bottom = defaultdict(int)
    for (x, y) in grid:
        this_bottom = grid.get_basin_bottom(x, y)
        positions_by_bottom[this_bottom] += 1
    positions_by_bottom.pop(None, None)
    basin_sizes = sorted(positions_by_bottom.values())
    return basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1] 

print(part_a())
print(part_b())
