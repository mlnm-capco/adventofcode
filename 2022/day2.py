import input


def calculate_game(theirs, ours):
    theirs_ord = index(theirs) + 1
    ours_ord = index(ours) + 1
    points = 3 if ours_ord == theirs_ord else 6 if ours_ord == (theirs_ord % 3) + 1 else 0
    print(f'{theirs} {ours}: {ours_ord} + {points} = {ours_ord + points}')
    return ours_ord + points


def calculate_move(theirs, result):
    their_index = index(theirs)
    adjustment = index(result) - 1  # -1, 0, 1
    ours = ['X', 'Y', 'Z'][(their_index + adjustment) % 3]
    return calculate_game(theirs, ours)


def index(move):
    return ['A', 'B', 'C', 'X', 'Y', 'Z'].index(move) % 3


def test():
    assert calculate_game('A', 'X') == 4
    assert calculate_game('B', 'X') == 1
    assert calculate_game('C', 'X') == 7
    assert calculate_game('A', 'Y') == 8
    assert calculate_game('B', 'Y') == 5
    assert calculate_game('C', 'Y') == 2
    assert calculate_game('A', 'Z') == 3
    assert calculate_game('B', 'Z') == 9
    assert calculate_game('C', 'Z') == 6


def test_moves():
    assert calculate_move('A', 'X') == 3
    assert calculate_move('B', 'X') == 1
    assert calculate_move('C', 'X') == 2
    assert calculate_move('A', 'Y') == 4
    assert calculate_move('B', 'Y') == 5
    assert calculate_move('C', 'Y') == 6
    assert calculate_move('A', 'Z') == 8
    assert calculate_move('B', 'Z') == 9
    assert calculate_move('C', 'Z') == 7


if __name__ == '__main__':
    # test()
    # test_moves()
    # exit(0)
    # values = input.read_strings(2, year=2022, from_file=True, filename='2022/day2test.txt')
    values = input.read_strings(2, year=2022)
    print(values)
    total = 0
    for v in values:
        score = calculate_move(v[:1], v[-1:])
        total += score
    print(total)
