from collections import Counter
import itertools

P1_START = 7
P2_START = 6

def dice_builder():
    yield from itertools.cycle(range(1, 101))

def part_a():
    pos1 = P1_START
    pos2 = P2_START
    score1 = score2 = roll_count = 0
    dice = dice_builder()
    p1_turn = True
    while True:
        roll_sum = sum(itertools.islice(dice, 3))
        roll_count += 3
        if p1_turn:
            pos1 = (pos1 + roll_sum) % 10
            score1 += (pos1 or 10)
        else:
            pos2 = (pos2 + roll_sum) % 10
            score2 += (pos2 or 10)
        p1_turn = not p1_turn
        if score1 >= 1000:
            return score2 * roll_count
        if score2 >= 1000:
            return score1 * roll_count


def get_result_frequencies():
    freq = Counter()
    for d1 in range(1, 4):
        for d2 in range(1, 4):
            for d3 in range(1, 4):
                freq[d1 + d2 + d3] += 1
    return freq

DICE_TOTALS = get_result_frequencies()

def play_turn(old_freqs):
    new_freqs = Counter()
    p1_wins = p2_wins = 0
    for world, freq in old_freqs.items():
        for total, total_freq in DICE_TOTALS.items():
            (score1, pos1, score2, pos2, p1_turn) = world
            freq_product = (freq * total_freq)

            if p1_turn:
                new_pos1 = ((pos1 + total) % 10) or 10            
                new_score1 = score1 + new_pos1
                if new_score1 >= 21:
                    p1_wins += freq_product
                    continue
                new_pos2 = pos2
                new_score2 = score2
            else:
                new_pos2 = ((pos2 + total) % 10) or 10
                new_score2 = score2 + new_pos2
                if new_score2 >= 21:
                    p2_wins += freq_product
                    continue
                new_pos1 = pos1
                new_score1 = score1

            new_freqs[(new_score1, new_pos1, new_score2, new_pos2, not p1_turn)] += freq_product
    return (new_freqs, p1_wins, p2_wins)


def part_b():
    # score1, pos1, score2, pos2, p1_turn
    freqs = {(0, P1_START, 0, P2_START, True): 1}
    p1_wins = p2_wins = 0
    while freqs:
        freqs, new_p1_wins, new_p2_wins = play_turn(freqs)
        p1_wins += new_p1_wins
        p2_wins += new_p2_wins
    return max(p1_wins, p2_wins)

print(part_a())
print(part_b())