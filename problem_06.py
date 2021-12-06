from collections import Counter, defaultdict
from pathlib import Path

def get_initial_counts():
    text = Path("problem_06.txt").read_text().strip()
    return Counter((int(x) for x in text.split(",")))

def iterate(counts):
    new_counts = defaultdict(int)
    zero_counts = counts.pop(0, 0)
    for countdown, count in counts.items():
        new_counts[countdown-1] = count
    new_counts[6] += zero_counts
    new_counts[8] += zero_counts
    return new_counts

def load_and_iterate(generations):
    counts = get_initial_counts()
    for _ in range(generations):
        counts = iterate(counts)
    return sum(counts.values())

def part_a():
    return load_and_iterate(80)

def part_b():
    return load_and_iterate(256)

print(part_a())
print(part_b())
