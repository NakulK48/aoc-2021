from collections import Counter
from pathlib import Path

def get_lines():
    text = Path("problem_03.txt").read_text().strip()
    return text.split("\n")

def part_a():
    lines = get_lines()
    line_length = len(lines[0])
    gamma_bits = []
    epsilon_bits = []
    for index in range(line_length):
        this_index_bits = [line[index] for line in lines]
        counts = Counter(this_index_bits)
        gamma_bits.append(max(counts, key=counts.get))
        epsilon_bits.append(min(counts, key=counts.get))
    gamma = int("".join(gamma_bits), 2)
    epsilon = int("".join(epsilon_bits), 2)
    return gamma * epsilon


def find_rating(lines, decision_key, tie_breaker):
    line_length = len(lines[0])
    for index in range(line_length):
        this_index_bits = [line[index] for line in lines]
        counts = Counter(this_index_bits)
        if counts["0"] == counts["1"]:
            correct_bit = tie_breaker
        else:
            correct_bit = decision_key(counts, key=counts.get)
        lines = [line for line in lines if line[index] == correct_bit]
        if len(lines) == 1:
            return int(lines[0], 2)
    raise RuntimeError("Multiple candidates remaining.")

def part_b():
    lines = get_lines()
    oxygen_cands = lines
    co2_cands = lines[:]
    
    oxygen_rating = find_rating(oxygen_cands, max, "1")
    co2_rating = find_rating(co2_cands, min, "0")

    return oxygen_rating * co2_rating

print(part_a())
print(part_b())
