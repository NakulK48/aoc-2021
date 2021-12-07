from collections import Counter, defaultdict
from pathlib import Path

def get_counts():
    text = Path("problem_07.txt").read_text().strip()
    return Counter((int(x) for x in text.split(",")))

def get_min_fuel(usage_calculator):
    counts = get_counts()
    best_target = None
    min_fuel = float("inf")
    for target_position in range(max(counts.keys())):
        fuel_required = 0
        for position, count in counts.items():
            distance = abs(position - target_position)
            fuel_per_crab = usage_calculator(distance)
            fuel_required += (fuel_per_crab * count)
        if fuel_required < min_fuel:
            best_target = target_position
            min_fuel = fuel_required
    print("Target:", best_target)
    return min_fuel

def part_a():
    return get_min_fuel(lambda x: x)

def triangular(base):
    return (base * (base + 1)) // 2

def part_b():
    return get_min_fuel(triangular)


print(part_a())
print(part_b())
