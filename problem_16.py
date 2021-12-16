from functools import reduce
import operator
from pathlib import Path
from typing import Callable, Dict, List, Tuple

def load_binary():
    hexadecimal = Path("problem_16.txt").read_text().strip()
    binary_str = bin(int(hexadecimal, 16))[2:]  # remove 0b
    return binary_str.zfill(len(hexadecimal) * 4)

Operator = Callable[[List[int]], int]

ID_TO_OPERATION: Dict[int, Operator] = {
    0: sum,
    1: (lambda subs: reduce(operator.mul, subs, 1)),
    2: min,
    3: max,
    5: (lambda subs: 1 if subs[0] > subs[1] else 0),
    6: (lambda subs: 1 if subs[0] < subs[1] else 0),
    7: (lambda subs: 1 if subs[0] == subs[1] else 0)
}

def parse_packet(remaining: str) -> Tuple[int, int, int]:
    version = int(remaining[:3], 2)
    type_id = int(remaining[3:6], 2)
    if type_id == 4: # literal packet
        index = 6
        number_bits = ""
        while True:
            next_group = remaining[index : index + 5]
            number_bits += next_group[1:] 
            index += 5
            if next_group[0] == "0":
                return (int(number_bits, 2), version, index)
    else:  # operator
        length_type_id = remaining[6]
        sub_values = []
        if length_type_id == "0":
            expected_length = int(remaining[7:22], 2)
            index = 22
            while index < (expected_length + 22):
                (sub_value, sub_version, sub_length) = parse_packet(remaining[index:])
                index += sub_length
                version += sub_version
                sub_values.append(sub_value)
        else:
            num_packets = int(remaining[7:18], 2)
            index = 18
            for _ in range(num_packets):
                (sub_value, sub_version, sub_length) = parse_packet(remaining[index:])
                index += sub_length
                version += sub_version
                sub_values.append(sub_value)
        
        return (ID_TO_OPERATION[type_id](sub_values), version, index)

def part_a():
    result, version, index = parse_packet(load_binary())
    return version

def part_b():
    result, version, index = parse_packet(load_binary())
    return result

print(part_a())
print(part_b())
