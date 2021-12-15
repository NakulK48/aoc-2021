from collections import Counter, defaultdict
from pathlib import Path
from typing import Tuple, Dict, List

def get_chain_and_rules() -> Tuple[List[str], Dict[str, str]]:
    text = Path("problem_14.txt").read_text().strip()
    chain, rules_str = text.split("\n\n")
    rules = {}
    for line in rules_str.split("\n"):
        pair, result = line.split(" -> ")
        rules[pair] = result
    return (list(chain), rules)


def part_a():
    chain, rules = get_chain_and_rules()
    for _ in range(10):
        index = 0
        while index < (len(chain) - 1):
            this_pair = chain[index] + chain[index + 1]
            chain.insert(index + 1, rules[this_pair])
            index += 2
    counter = Counter(chain)
    return max(counter.values()) - min(counter.values())


def get_pair_counts(chain: List[str]):
    return Counter(
        chain[i] + chain[i+1]
        for i in range(len(chain) - 1)
    )


def part_b():
    chain, rules = get_chain_and_rules()
    pair_counts = get_pair_counts(chain)
    char_counts = Counter(chain)
    for _ in range(40):
        new_pair_counts = defaultdict(int)
        for pair, current_freq in pair_counts.items():
            new_element = rules[pair]
            char_counts[new_element] += current_freq
            new_pair_counts[pair[0] + new_element] += current_freq
            new_pair_counts[new_element + pair[1]] += current_freq
        pair_counts = new_pair_counts

    return (max(char_counts.values()) - min(char_counts.values()))

print(part_a())
print(part_b())
