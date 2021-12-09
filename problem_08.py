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

UNAMBIGUOUS_LENGTHS = {
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}

def part_a():
    return sum(
        1
        for _, output in get_signals_and_outputs()
        for digit in output if len(digit) in UNAMBIGUOUS_LENGTHS
    )

def segment_overlap(first, second):
    return len(set(first) & set(second))

def part_b():
    total = 0
    for signal, output in get_signals_and_outputs():
        segments_to_digit = {}
        digit_to_segments = {}
        for segments in signal:
            length = len(segments)
            if length in UNAMBIGUOUS_LENGTHS:
                digit = UNAMBIGUOUS_LENGTHS[length]
                segments_to_digit[segments] = digit
                digit_to_segments[digit] = segments
        for segments in signal:
            length = len(segments)
            if length not in (5, 6):
                continue
            overlap1 = segment_overlap(segments, digit_to_segments[1])
            overlap4 = segment_overlap(segments, digit_to_segments[4])

            segments_to_digit[segments] = {
                # length, overlap1, overlap4
                (6, 1, 3): 6,
                (6, 2, 3): 0,
                (6, 2, 4): 9,
                (5, 1, 2): 2,
                (5, 2, 3): 3,
                (5, 1, 3): 5
            }[length, overlap1, overlap4]
        assert sorted(segments_to_digit.values()) == list(range(10))

        output_digits = [str(segments_to_digit[segments]) for segments in output]
        total += int("".join(output_digits))
    return total

print(part_a())
print(part_b())
