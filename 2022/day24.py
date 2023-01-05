from copy import copy

from numpy import int_, ndarray

import input
import numpy as np
from mytypes.grid import Point, Grid, get_neighbours


def part1(grid: ndarray, start: Point, by_exit: Point):
    minute = -1
    queue = [(start, 0)]
    while queue:
        current, minute_ = queue.pop(0)
        # if start.manhattan_distance(current) * 8 < minute:
        #     continue
        if current == by_exit:
            print(f'------ Minute {minute}: queue: {len(queue)} -------')
            print_grid(grid, current)
            grid = move_blizzards(grid)
            return grid, minute_ + 1
        if minute_ > minute:
            print(f'------ Minute {minute}: queue: {len(queue)} -------')
            # print_grid(grid, current)
            grid = move_blizzards(grid)
            minute = minute_
        candidates = get_neighbours(grid, current.x, current.y)
        candidates.append(current)
        for p in candidates:
            if grid[p.y][p.x] == 0:
                if not (p, minute + 1) in queue:
                    queue.append((p, minute + 1))


def move_blizzards(grid: ndarray):
    new_grid = np.zeros_like(grid)
    new_grid[0, :] = -1
    new_grid[-1, :] = -1
    new_grid[:, 0] = -1
    new_grid[:, -1] = -1
    new_grid[0, 1] = 0
    new_grid[-1, -2] = 0

    for row in range(1, grid.shape[0] - 1):
        for col in range(1, grid.shape[1] - 1):
            cell = grid[row][col]
            if cell == 0:
                continue
            if int(cell) & 1 == 1:
                new_grid[row, col + 1 if col < grid.shape[1] - 2 else 1] += 1
            if int(cell) & 2 == 2:
                new_grid[row + 1 if row < grid.shape[0] - 2 else 1, col] += 2
            if int(cell) & 4 == 4:
                new_grid[row, col - 1 if col > 1 else grid.shape[1] - 2] += 4
            if int(cell) & 8 == 8:
                new_grid[row - 1 if row > 1 else grid.shape[0] - 2, col] += 8
    return new_grid


def initialise_grid(grid: Grid):
    arr = np.zeros(shape=(grid.height(), grid.width()), dtype=int_)
    for j in range(0, grid.height()):
        for i in range(0, grid.width()):
            if grid[j][i] == '.':
                arr[j][i] = 0
            elif grid[j][i] == '#':
                arr[j][i] = -1
            else:
                arr[j][i] = 2 ** ('>v<^'.index(grid[j][i]))
    return arr


def print_grid(grid: ndarray, pos: Point = None):
    if pos is not None:
        grid[pos.y, pos.x] = 16
    for j in range(grid.shape[0]):
        print(''.join(['#.>v2<223^2232334E'[val + 1] for val in grid[j]]))
    if pos is not None:
        grid[pos.y, pos.x] = 0


if __name__ == '__main__':
    # grid = input.read_grid(24, year=2022, from_file=True, filename='2022/day24test.txt', as_ints=False)
    grid = input.read_grid(24, year=2022, as_ints=False)
    print(grid)

    start = Point(1, 0)
    grid = initialise_grid(grid)
    print(grid)

    # print_grid(grid, pos)
    # grid = move_blizzards(grid)
    # pos = Point(1, 1)
    print_grid(grid, start)

    by_exit = Point(grid.shape[1] - 2, grid.shape[0] - 2)
    exit_ = Point(grid.shape[1] - 1, grid.shape[0] - 2)

    grid, total = part1(grid, start, by_exit)
    print(f'To exit: {total}')
    grid, to_start = part1(grid, exit_, Point(1, 1))
    print(to_start)
    grid, second_run = part1(grid, start, by_exit)
    print(f'Second run: {second_run}')
    print(f'Total: {total} + {to_start + 1} + {second_run + 1} = {total + to_start + 1 + second_run + 1}')
    # 974