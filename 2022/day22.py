import input
import re
import operator

from mytypes.grid import parse_grid, Grid


def parse_moves(source: str):
    return re.findall('[0-9]+|[RLDU]', source)


def do_move(grid, moves, pos, dir):
    move_dict = {2: (-1, 0), 0: (1, 0), 3: (0, -1), 1: (0, 1)}
    new_dir = dir
    for _ in range(moves):
        delta = move_dict[dir]
        new_pos = (pos[0] + delta[0], pos[1] + delta[1])

        if new_pos[0] < 0 or new_pos[0] >= grid.width() or new_pos[1] < 0 or new_pos[1] >= grid.height() or len(grid[new_pos[1]][new_pos[0]].strip()) == 0:
            new_pos, new_dir = wrap2(pos, new_pos, dir)
        dest = grid[new_pos[1]][new_pos[0]]
        if dest == '#':
            return pos, dir
        pos = new_pos
        dir = new_dir
    return pos, dir


def wrap(grid, pos, new_pos, dir):
    if dir == 0:
        new_pos = (min(grid[pos[1]].index('.'), grid[pos[1]].index('#')), new_pos[1])
    elif dir == 2:
        new_pos = (
        len(grid[pos[1]]) - 1 - min(grid[pos[1]][::-1].index('.'), grid[pos[1]][::-1].index('#')), new_pos[1])
    elif dir == 1:
        for row in range(grid.height()):
            if len(grid[row][new_pos[0]].strip()) > 0:
                new_pos = (new_pos[0], row)
                break
    elif dir == 3:
        for row in range(grid.height() - 1, 0, -1):
            if len(grid[row][new_pos[0]].strip()) > 0:
                new_pos = (new_pos[0], row)
                break
    return new_pos


def wrap2(pos, new_pos, dir):
    x, y = pos[0], pos[1]
    if dir == 0:
        if y < 50:
            new_pos = (99, 149 - y)
            dir = 2
        elif y < 100:
            new_pos = (50 + y, 49)
            dir = 3
        elif y < 150:
            new_pos = (149, 149 - y)
            dir = 2
        else:
            new_pos = (y - 100, 149)
            dir = 3
    elif dir == 2:
        if y < 50:
            new_pos = (0, 149 - y)
            dir = 0
        elif y < 100:
            new_pos = (y - 50, 100)
            dir = 1
        elif y < 150:
            new_pos = (50, 149 - y)
            dir = 0
        else:
            new_pos = (y - 100, 0)
            dir = 1
    elif dir == 1:
        if x < 50:
            new_pos = (x + 100, 0)
            dir = 1
        elif x < 100:
            new_pos = (49, x + 100)
            dir = 2
        else:
            new_pos = (99, x - 50)
            dir = 2
    elif dir == 3:
        if x < 50:
            new_pos = (50, x + 50)
            dir = 0
        elif x < 100:
            new_pos = (0, x + 100)
            dir = 0
        else:
            new_pos = (x - 100, 199)
            dir = 3
    return new_pos, dir


def part1(grid: Grid, moves: list[str], pos: tuple[int, int], dir: int):
    for move in moves:
        if move == 'R':
            dir = (dir + 1) % 4
        elif move == 'L':
            dir = (dir - 1) % 4
        else:
            pos, dir = do_move(grid, int(move), pos, dir)
    return pos, dir


def pad_grid(source):
    max_len = max([len(line) for line in source])
    return [line.rstrip().ljust(max_len, ' ') for line in source]


if __name__ == '__main__':
    # source = input.read_strings(22, year=2022, from_file=True, filename='2022/day22test.txt', strip=False)
    source = input.read_strings(22, year=2022, strip=False)
    print(source)
    print(len(source))
    grid = Grid(pad_grid(source[:-2]), as_ints=False)

    moves = parse_moves(source[-1])
    print(grid)
    print(moves)
    pos = (grid[0].index('.'), 0)
    dir = 0
    print(pos, dir)
    final_pos, dir = part1(grid, moves, pos, dir)
    print(final_pos, dir)
    result = (final_pos[1] + 1) * 1000 + (final_pos[0] + 1) * 4 + dir
    print(result)
    # 121302 too low
    # 191010

    # pt2
    # 44394 too low
