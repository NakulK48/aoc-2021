from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set

def get_connections() -> Dict[str, List[str]]:
    conns = defaultdict(list)
    lines = Path("problem_12.txt").read_text().strip().split("\n")
    for line in lines:
        first, second = line.split("-")
        conns[first].append(second)
        conns[second].append(first)
    return conns

START = "start"
END = "end"

def part_a():
    connections = get_connections()
    route_count = 0

    def traverse(current: str, visited: Set[str]):
        nonlocal route_count
        if current == END:
            route_count += 1
            return
        new_visited = (visited | {current}) if current.islower() else visited
        for next_cave in connections[current]:
            if next_cave not in new_visited:
                traverse(next_cave, new_visited)
    
    traverse(START, set())
    return route_count

def part_b():
    connections = get_connections()
    route_count = 0

    def traverse(current: str, visited: Set[str], revisited_small: bool):
        nonlocal route_count
        if current == END:
            route_count += 1
            return
        new_visited = (visited | {current}) if current.islower() else visited
        for next_cave in connections[current]:
            if next_cave == START:
                continue
            if next_cave not in new_visited:
                traverse(next_cave, new_visited, revisited_small)
            elif not revisited_small:
                traverse(next_cave, new_visited, revisited_small=True)

    traverse(START, set(), revisited_small=False)
    return route_count

print(part_a())
print(part_b())
