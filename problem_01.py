from pathlib import Path

def get_nums():
    text = Path("problem_01.txt").read_text().strip()
    return [int(line) for line in text.split("\n")]

def part_a():
    nums = get_nums()
    count = 0
    for i in range(1, len(nums)):
        if nums[i] > nums[i-1]:
            count += 1
    return count

def part_b():
    nums = get_nums()
    count = 0
    for range_end in range(3, len(nums)):
        if nums[range_end] > nums[range_end-3]:
            count += 1
    return count


print(part_a())
print(part_b())
