import input
import re
from numpy import sign

from mytypes.grid import Grid


def parse_move(raw: str):
    result = re.match('([RLUD]) ([0-9]*)', raw)
    return result[1], int(result[2])


def move_knot(head, tail):
    if abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1:
        return tail

    new_tail = tail
    if abs(tail[0] - head[0]) >= 1:
        new_tail = (tail[0] - sign(tail[0] - head[0]), tail[1])
    if abs(tail[1] - head[1]) >= 1:
        new_tail = (new_tail[0], tail[1] - sign(tail[1] - head[1]))
    return new_tail


def process_moves(moves: list[tuple[str, int]], no_knots: int = 2):
    touched = set()
    dir = {'D': (0, 1), 'U': (0, -1), 'L': (-1, 0), 'R': (1, 0)}
    knots = [(0, 0) for _ in range(0, no_knots)]
    touched.add((0, 0))
    for move in moves:
        for _ in range(1, move[1] + 1):
            knots[0] = tuple([sum(tup) for tup in zip(knots[0], dir[move[0]])])
            # print(f'Head: {knots[0]}')
            for i in range(1, no_knots):
                knots[i] = move_knot(knots[i - 1], knots[i])
            # print(f'Tail: {knots[no_knots - 1]}')
            touched.add(knots[no_knots - 1])
            render(knots, touched)

    return len(touched)


def render(knots: list[tuple[int, int]], touched: set[tuple[int, int]]):
    print('-----')
    min_x = min(min([t[0] for t in touched]), min([knot[0] for knot in knots]))
    max_x = max(max([t[0] for t in touched]), max([knot[0] for knot in knots]))
    min_y = min(min([t[1] for t in touched]), min([knot[1] for knot in knots]))
    max_y = max(max([t[1] for t in touched]), max([knot[1] for knot in knots]))
    grid = [[' ' for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]
    i = 0
    for knot in knots:
        if grid[knot[1] - min_y][knot[0] - min_x] == ' ':
            grid[knot[1] - min_y][knot[0] - min_x] = str(i + 1)
        i += 1
    for cell in touched:
        if grid[cell[1] - min_y][cell[0] - min_x] == ' ':
            grid[cell[1] - min_y][cell[0] - min_x] = '#'
    print(*grid, sep='\n')


if __name__ == '__main__':
    raw_moves = input.read_strings(9, year=2022, from_file=True, filename='2022/day9test2.txt')
    # raw_moves = input.read_strings(9, year=2022)
    moves = [parse_move(move) for move in raw_moves]
    print(moves)
    print(process_moves(moves, 10))
