import input
from collections import deque
from mytypes.vent import Point
import itertools


def steps(grid, steps):
    total = 0
    for i in range(0, steps):
        flashes = step(grid)
        print(f'Step {i}, flashes: {flashes}')
        total += flashes
        # print(f"Step {i + 1}:")
        # print_grid(grid)
    return total


def step(grid):
    for row in grid:
        row[:] = [o + 1 for o in row]
    return process_flashes(grid)


def first_sync(grid):
    flashers = 0
    i = 0
    while flashers < len(grid) * len(grid[0]):
        i += 1
        flashers = step(grid)
        print(f'Step {i}, flashes: {flashers}')
    return i


def process_flashes(grid):
    flashers = deque()
    flashed = set()
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            if grid[y][x] == 10:
                flashers.append(Point(x, y))
    while len(flashers) > 0:
        flasher = flashers.pop()
        if flasher in flashed:
            continue
        flashed.add(flasher)
        for neighbour in get_neighbours(grid, flasher.x, flasher.y):
            grid[neighbour.y][neighbour.x] += 1
            if grid[neighbour.y][neighbour.x] > 9 and neighbour not in flashed:
                flashers.append(neighbour)
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            if grid[y][x] >= 10:
                grid[y][x] = 0
    return len(flashed)


def get_neighbours(grid, x, y):
    neighbours = list(itertools.product(range(x - 1, x + 2), range(y - 1, y + 2)))
    neighbours.remove((x, y))
    return [Point(p[0], p[1]) for p in neighbours if 0 <= p[0] < len(grid[0]) and 0 <= p[1] < len(grid)]


def print_grid(grid):
    for row in grid:
        print(', '.join(map(str, row)))


if __name__ == '__main__':
    grid = input.read_grid(11, from_file=False)
    print_grid(grid)
    # print(get_neighbours(grid, 9, 9))
    #print(steps(grid, 100))  # s/b 1656
    print(f'Sync={first_sync(grid)}')
    # print(steps(grid, 2))
    # print_grid(grid)
    # 214 too low
    # 2330 too high

    # 89-7475445
    # 5089086933
    # 8597888395
    # 8363669379
    # 8579608600

    # 5278635756
    # 3287952832
    # 7993992245
    # 5957959665
    # 6394862637

    # 8807476555
    # 5089087054
    # 8597889608
    # 8485769600
    # 8700908800
    # 6600088989
    # 6800005943
    # 0000007456
    # 9000000876
    # 8700006848
