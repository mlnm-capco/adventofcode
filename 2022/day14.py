import numpy

import input
from mytypes.grid import Grid, Point

ENTRY_POINT = 500


def parse_points(grid: Grid, point1, point2):
    x = point1[0]
    y = point1[1]
    grid[y][x] = '#'
    while x != point2[0] or y != point2[1]:
        x += numpy.sign(point2[0] - point1[0])
        y += numpy.sign(point2[1] - point1[1])
        grid[y][x] = '#'
    # print(grid)
    # print('---')


def parse_segments(segments: list[list[tuple[int, int]]], max_x: int, max_y: int, entry_x: int):
    raw_grid = [['.'] * (max_x + 1) for _ in range(0, max_y + 1)]
    grid = Grid(raw_grid, as_ints=False)
    grid[0][entry_x] = '+'
    for segment in segments:
        # [(4, 4), (4, 6), (2, 6)]
        for i in range(len(segment) - 1):
            parse_points(grid, segment[i], segment[i + 1])
    print(grid)
    return grid


def drop_sand(grid: Grid, entry_x: int):
    x, y, count = entry_x, 0, 0
    while True:
        if x < 0 or y >= grid.height() - 1:
            break
        next_down = grid[y + 1][x]
        if next_down == '.':
            y += 1
            continue
        elif next_down == 'o' or next_down == '#':
            if grid[y + 1][x - 1] == '.':
                y += 1
                x -= 1
            elif grid[y + 1][x + 1] == '.':
                y += 1
                x += 1
            else:
                grid[y][x] = 'o'
                count += 1
                if y == 0 and x == entry_x:
                    break
                x, y = entry_x, 0
    print('---')
    print(grid)
    print(count)
    return count


def drop_sand2(grid: Grid, entry_x: int):
    x, y, count, off_left, off_right = entry_x, 0, 0, 0, 0
    while True:

        if x < 0 or x >= grid.width():
            break

        # print(f'{x, y}')
        next_down = grid[y + 1][x]
        if next_down == '.':
            y += 1
            continue
        elif next_down == 'o' or next_down == '#':
            if y < grid.height() - 1 and grid[y + 1][x - 1] == '.':
                y += 1
                x -= 1
            elif y < grid.height() - 1 and grid[y + 1][x + 1] == '.':
                y += 1
                x += 1
            else:
                grid[y][x] = 'o'
                count += 1
                if y == 0 and x == entry_x:
                    break
                x, y = entry_x, 0
    print('---')
    print(grid)
    print(count)
    return count


if __name__ == '__main__':
    # raw = input.read_strings(14, year=2022, from_file=True, filename='2022/day14test.txt')
    raw = input.read_strings(14, year=2022)
    segments = [[tuple([int(x) for x in item.strip().split(',')]) for item in segment] for segment in [path for path in [line.split('->') for line in raw]]]

    max_y = max([x[1] for segment in segments for x in segment])

    # pt 1
    min_x = min([x[0] for segment in segments for x in segment])
    max_x = max([x[0] for segment in segments for x in segment])

    # pt 2
    # min_x, max_x = 501 - max_y, 501 + max_y

    entry_x = ENTRY_POINT - min_x
    print(segments)
    print(min_x)
    print(segments)

    print(f'Min X: {min_x}')
    print(f'Max X: {max_x}')
    print(f'Max Y: {max_y}')
    print(f'Entry: {entry_x}')

    for segment in segments:
        for i in range(len(segment)):
            segment[i] = (segment[i][0] - min_x, segment[i][1])
    print(segments)

    max_y += 1
    grid = parse_segments(segments, max_x - min_x, max_y, entry_x)
    grid.grid.append('#' * grid.width())
    print(grid)
    drop_sand(grid, entry_x)
    # drop_sand2(grid, entry_x)
    grid.plot()
