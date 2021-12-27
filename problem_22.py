from pathlib import Path

def parse_range_str(range_str: str):
    start_str, end_str = range_str[2:].split("..")
    return (int(start_str), int(end_str))


def load_instructions():
    lines = Path("problem_22.txt").read_text().strip().split("\n")
    for line in lines:
        change, ranges_str = line.split(" ")
        x_str, y_str, z_str = ranges_str.split(",")
        x_range = parse_range_str(x_str)
        y_range = parse_range_str(y_str)
        z_range = parse_range_str(z_str)
        yield (change, x_range, y_range, z_range)

def true_range(start, end):
    true_start = max(start, -50)
    true_end = min(end, 50)
    return range(true_start, true_end + 1)

def part_a():
    lit_cells = set()
    for (change, x_range, y_range, z_range) in load_instructions():
        if change == "on":
            for x in true_range(*x_range):
                for y in true_range(*y_range):
                    for z in true_range(*z_range):
                        lit_cells.add((x, y, z))
        else:
            for x in true_range(*x_range):
                for y in true_range(*y_range):
                    for z in true_range(*z_range):
                        lit_cells.discard((x, y, z))
    return len(lit_cells)


def part_b():
    lit_cells = set()
    for (change, (x1, x2), (y1, y2), (z1, z2)) in load_instructions():
        pass

print(part_b())