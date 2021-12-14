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


def get_pair_to_frequency(chain: List[str]):
    return Counter(
        chain[i] + chain[i+1]
        for i in range(len(chain) - 1)
    )


def part_b():
    chain, rules = get_chain_and_rules()
    last_char = chain[-1]
    pair_to_frequency = get_pair_to_frequency(chain)
    for _ in range(40):
        new_pair_to_frequency = defaultdict(int)
        for pair, current_freq in pair_to_frequency.items():
            new_element = rules[pair]
            new_pair_to_frequency[pair[0] + new_element] += current_freq
            new_pair_to_frequency[new_element + pair[1]] += current_freq
        pair_to_frequency = new_pair_to_frequency
    
    # only count the first in the pair to avoid double counting
    char_to_frequency = defaultdict(int)
    for pair, pair_frequency in pair_to_frequency.items():
        char_to_frequency[pair[0]] += pair_frequency

    # the last char is never first in the pair
    char_to_frequency[last_char] += 1

    max_freq = max(char_to_frequency.values())
    min_freq = min(char_to_frequency.values())
    return (max_freq - min_freq)

print(part_a())
print(part_b())
