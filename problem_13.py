from pathlib import Path
from typing import List, Set, Tuple

Point = Tuple[int, int]
Fold = Tuple[str, int]

def load_points_and_folds() -> Tuple[Set[Point], List[Fold]]:
    text = Path("problem_13.txt").read_text().strip()
    point_str, fold_str = text.split("\n\n")
    points = set()
    folds = []
    for line in point_str.split("\n"):
        x_str, y_str = line.split(",")
        points.add((int(x_str), int(y_str)))

    for line in fold_str.split("\n"):
        axis, pos_str = line.replace("fold along ", "").split("=")
        folds.append((axis, int(pos_str)))

    return (points, folds)


def fold_x(points: Set[Point], fold_position: int) -> Set[Point]:
    new_points = set()
    for (x, y) in points:
        if x < fold_position:
            new_points.add((x, y))
        else:
            new_x = fold_position - (x - fold_position)
            new_points.add((new_x, y))
    return new_points

def fold_y(points: Set[Point], fold_position: int) -> Set[Point]:
    new_points = set()
    for (x, y) in points:
        if y < fold_position:
            new_points.add((x, y))
        else:
            new_y = fold_position - (y - fold_position)
            new_points.add((x, new_y))
    return new_points

class Grid:
    def __init__(self, points: Set[Point]):
        height = max(y for (x, y) in points) + 1
        width = max(x for (x, y) in points) + 1
        self.grid = [[False for _ in range(width)] for __ in range(height)]
        for (x, y) in points:
            self.grid[y][x] = True

    def __str__(self):
        result = ""
        for row in self.grid:
            for cell in row:
                result += ("X" if cell else " ")
            result += "\n"
        return result


def part_a():
    points, folds = load_points_and_folds()
    for (axis, fold_pos) in [folds[0]]:
        points = fold_x(points, fold_pos) if axis == "x" else fold_y(points, fold_pos)
    return len(points)

def part_b():
    points, folds = load_points_and_folds()
    for (axis, fold_pos) in folds:
        points = fold_x(points, fold_pos) if axis == "x" else fold_y(points, fold_pos)
    return Grid(points)


print(part_a())
print(part_b())