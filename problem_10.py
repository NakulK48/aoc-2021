from collections import deque
from pathlib import Path

def get_lines():
    return Path("problem_10.txt").read_text().strip().split("\n")

OPENING_TO_CLOSING = {
    "(": ")", "[": "]", "{": "}", "<": ">"
}

CLOSING_TO_SCORE_A = {
    ")": 3, "]": 57, "}": 1197, ">": 25137
}

def part_a():
    lines = get_lines()
    score = 0
    for line in lines:
        stack = deque()
        for char in line:
            if char in OPENING_TO_CLOSING:
                stack.append(char)
                continue
            last_opener = stack.pop()
            if char != OPENING_TO_CLOSING[last_opener]:
                score += CLOSING_TO_SCORE_A[char]
    return score

CLOSING_TO_SCORE_B = {
    ")": 1, "]": 2, "}": 3, ">": 4
}

def part_b():
    lines = get_lines()
    scores = []
    for line in lines:
        line_score = 0
        stack = deque()
        for char in line:
            if char in OPENING_TO_CLOSING:
                stack.append(char)
                continue
            last_opener = stack.pop()
            if char != OPENING_TO_CLOSING[last_opener]:
                break # invalid line; no score
        else:  # if we didn't break
            while stack:
                opener = stack.pop()
                closer_score = CLOSING_TO_SCORE_B[OPENING_TO_CLOSING[opener]]
                line_score = (line_score * 5) + closer_score
            scores.append(line_score)
    scores.sort()
    return scores[len(scores)//2]

print(part_b())
