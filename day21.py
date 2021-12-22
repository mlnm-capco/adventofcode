
def part1():
    # brute force
    scores = [0, 0]
    positions = [7, 2]
    turn = die = i = 0
    while scores[0] < 1000 and scores[1] < 1000:
        move = die * 3 + 6
        die += 3
        positions[turn] = (positions[turn] - 1 + move) % 10 + 1
        scores[turn] += positions[turn]
        print(f'Die: {die}, positions: {positions}, scores: {scores}')
        i += 1
        turn = 1 - turn
    print(die, scores)
    if scores[0] >= 1000:
        print(scores[1] * die)
    else:
        print(scores[0] * die)
    # 861 [1008, 788]
    # 678468


def play(p1, p2):
    return sum([roll(p1, 0, p2, 0, i, 1) * combos[i] for i in range(3, 10)])


def roll(active_pos, active_score, other_pos, other_score, die, p1_turn):
    key = f'{active_pos:02}{active_score:02}{other_pos:02}{other_score:02}{die}{p1_turn}'
    if key in memo:
        return memo[key]
    active_pos = ((active_pos - 1 + die) % 10) + 1
    active_score += active_pos
    if active_score >= 21:
        memo[key] = p1_turn
        return p1_turn

    wins = sum([roll(other_pos, other_score, active_pos, active_score, i, 1 - p1_turn) * combos[i] for i in range(3, 10)])
    memo[key] = wins
    return wins


if __name__ == '__main__':
    combos = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    memo = {}
    print(play(7, 2))
    print(memo)
