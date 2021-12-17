import itertools
from pathlib import Path

def get_target():
    text = Path("problem_17.txt").read_text().strip()
    xstr, ystr = text.replace("target area: ", "").split(", ")
    xmin, xmax = xstr.replace("x=", "").split("..")
    ymin, ymax = ystr.replace("y=", "").split("..")
    return [int(n) for n in (xmin, xmax, ymin, ymax)]


def max_ypos(xvel_initial, yvel_initial, target):
    xpos = ypos = max_ypos_so_far = 0
    xvel = xvel_initial
    yvel = yvel_initial
    (xmin, xmax, ymin, ymax) = target
    while True:
        xpos += xvel
        ypos += yvel
        max_ypos_so_far = max(max_ypos_so_far, ypos)
        xvel = max(xvel-1, 0)
        yvel -= 1
        if xpos > xmax or ypos < ymin:
            return None  # overshot
        if xpos >= xmin and ypos <= ymax:
            return max_ypos_so_far


def part_a():
    target = (xmin, xmax, ymin, ymax) = get_target()
    for yvel_initial in range(200, 0, -1):
        for xvel_initial in range(xmax):
            maximum_height = max_ypos(xvel_initial, yvel_initial, target)
            if maximum_height is not None:
                print(yvel_initial, xvel_initial)
                return maximum_height


def part_b():
    target = (xmin, xmax, ymin, ymax) = get_target()
    count = 0
    for yvel_initial in range(ymin, 200):
        for xvel_initial in range(xmax + 1):
            if max_ypos(xvel_initial, yvel_initial, target) is not None:
                count += 1
    return count

print(part_a())
print(part_b())

