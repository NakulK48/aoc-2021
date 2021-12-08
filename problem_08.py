from pathlib import Path

def get_signals_and_outputs():
    text = Path("problem_08.txt").read_text().strip()
    result = []
    for line in text.split("\n"):
        (sig_str, output_str) = line.split(" | ")
        sig_list = sig_str.split()
        output_list = output_str.split()
        sorted_sig_list = ["".join(sorted(sig)) for sig in sig_list]
        sorted_output_list = ["".join(sorted(output)) for output in output_list]
        result.append((sorted_sig_list, sorted_output_list))

    return result

UNAMBIGUOUS_LENGTHS = (2, 3, 4, 7)

def part_a():
    signals_and_outputs = get_signals_and_outputs()
    total = 0
    for _, output in signals_and_outputs:
        for digit in output:
            if len(digit) in UNAMBIGUOUS_LENGTHS:
                total += 1
    return total

# Encode as:

#  1
# 2 3
#  4
# 5 6
#  7

SEGMENTS_TO_DIGIT = {
    "36": 1,
    "13457": 2,
    "134567": 3,
    "2346": 4,
    "12467": 5,
    "124567": 6,
    "136": 7,
    "1234567": 8,
    "123467": 9
}

LENGTH_TO_DIGITS = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8]
}

def segment_overlap(first, second):
    return len(set(first) & set(second))

"""
a cde g 2
a cd fg 3
ab d fg 5

 bcd f  4
"""

def part_b():
    signals_and_outputs = get_signals_and_outputs()
    total = 0
    for signal, output in signals_and_outputs:
        segments_to_digit = {}
        digit_to_segments = {}
        for segments in signal:
            length = len(segments)
            if length in UNAMBIGUOUS_LENGTHS:
                [digit] = LENGTH_TO_DIGITS[length]
                segments_to_digit[segments] = digit
                digit_to_segments[digit] = segments
        for segments in signal:
            if len(segments) == 6:
                # 0, 6 or 9
                overlap1 = segment_overlap(segments, digit_to_segments[1])
                if overlap1 == 1:
                    digit = 6
                else:
                    overlap4 = segment_overlap(segments, digit_to_segments[4])
                    digit = 0 if overlap4 == 3 else 9
                segments_to_digit[segments] = digit
            if len(segments) == 5:
                # 2, 3 or 5
                overlap4 = segment_overlap(segments, digit_to_segments[4])
                if overlap4 == 2:
                    digit = 2
                else:
                    overlap1 = segment_overlap(segments, digit_to_segments[1])
                    digit = 3 if overlap1 == 2 else 5
                segments_to_digit[segments] = digit
        assert sorted(segments_to_digit.values()) == list(range(10))
        
        output_digits = ""
        for segments in output:
            output_digits += str(segments_to_digit[segments])
        total += int(output_digits)
    return total

print(part_a())
print(part_b())
