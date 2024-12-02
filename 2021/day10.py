import input
from collections import deque


pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
pt1_scores = {')': 3, ']': 57, '}': 1197, '>': 25137}


def validate_line(line: str):
    last_open = deque()
    for char in line:
        if char in '<{[(':
            last_open.append(char)
            continue
        last = last_open.pop()
        if char != pairs[last]:
            return pt1_scores[char]
    return 0


def autocomplete(line: str):
    last_open = deque()
    for char in line:
        if char in '<{[(':
            last_open.append(char)
        else:
            last_open.pop()
    score = 0
    scores = {'(': 1, '[': 2, '{': 3, '<': 4}
    print(last_open)
    while len(last_open) > 0:
        current = last_open.pop()
        score *= 5
        score += scores[current]
    return score


def pt1(lines):
    return sum([validate_line(line) for line in lines])


def pt2(lines):
    print(len(lines))
    lines = [line for line in lines if validate_line(line) == 0]
    print(len(lines))
    results = [autocomplete(line) for line in lines]
    print(results)
    return sorted(results)[int(len(results) / 2)]
    # 288767662093 too high
    # 30269419813 too high
    # 2904180541


if __name__ == '__main__':
    lines = input.read_strings(10)
    print(lines)
    print(pt1(lines))
    print(pt2(lines))
    # pt1 = 311895
