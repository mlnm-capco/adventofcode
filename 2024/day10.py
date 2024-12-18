from collections import deque

import input
from mytypes.grid import Point


def part_one(_grid):
    total = 0
    for j in range(0, _grid.height()):
        for i in range(0, _grid.width()):
            # print(f'{i},{j}: {_grid[j][i]}')
            if _grid[j][i] == 0:
                total += get_trailheads(_grid, i, j)
    return total


def get_trailheads(_grid, i, j):
    stack = deque([(Point(i, j), 0)])
    trailheads: set[Point] = set()
    while len(stack) > 0:
        current_point, current = stack.pop()
        neighbours = [(n, current + 1) for n in _grid.get_all_neighbours(current_point.x, current_point.y) if _grid.get(n) == current + 1]
        if current + 1 == 9:
            for n in neighbours:
                if n not in trailheads:
                    trailheads.add(n[0])
            continue
        stack.extend(neighbours)
    return len(trailheads)

def get_trailheads_2(_grid, i, j):
    stack = deque([(Point(i, j), 0)])
    total = 0
    while len(stack) > 0:
        current_point, current_depth = stack.pop()
        next_steps = [(n, current_depth + 1) for n in _grid.get_point_neighbours(current_point) if _grid.get(n) == current_depth + 1]
        if current_depth + 1 == 9:
            total += len(next_steps)
        else:
            stack.extend(next_steps)
    return total


def part_two(_grid):
    total = 0
    for j in range(0, _grid.height()):
        for i in range(0, _grid.width()):
            if _grid[j][i] == 0:
                total += get_trailheads_2(_grid, i, j)
    return total


# part one = 617
# part two = 1477
if __name__ == '__main__':

    day, test = 10, False
    input = input.read_grid(day, year=2024, from_file=test, as_ints=True, filename=f'../input/2024/day{day}test.txt')

    print(f'Input: \n{input}')

    result = part_one(input)
    print(f'Part 1: {result}')
    # assert result == 36

    result2 = part_two(input)
    print(f'Part 2: {result2}')
    # assert result2 == 81


