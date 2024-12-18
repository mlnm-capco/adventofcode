import math
from collections import deque
from copy import copy

import input
from mytypes.grid import Direction, Point, Grid


def part_one(input):
    return solve_maze(input)[0]


def part_two(input, points: list[Point], pre_dropped: int):
    _, routes = solve_maze(input)
    for point in points[pre_dropped:]:
        for route in routes:
            if point in route:
                routes.remove(route)
        if len(routes) == 0:
            return point
    return None

def part_two2(input, width, height):
    grid, points = parse_input(input, width, height, len(input))
    for i in range(len(points) - 1, 0, -1):
        p = points[i]
        grid[p.y][p.x] = '.'
        if not is_solvable(grid):
            continue
        else:
            print(p)
            return p
    return None


def parse_input(input, width, height, blocks: int):
    grid = Grid.fill('.', width, height)
    points = []
    for line in input:
        x, y = line.split(',')
        points.append(Point(x, y))
    grid.populate_points('#', points[0: blocks])
    return grid, points

def is_solvable(grid: Grid, pos: Point = Point(0,0)):
    stack = deque([(pos)])
    visited = {pos}
    while len(stack) > 0:
        current_pos = stack.pop()
        if current_pos == Point(grid.width() - 1, grid.height() - 1):
            return True

        next_moves = [n for n in grid.get_point_neighbours(current_pos) if grid.get(n) == '.' and n not in stack and n not in visited]
        for n in next_moves:
            visited.add(n)
            stack.append(n)
    return False

def solve_maze(grid: Grid, pos: Point = Point(0,0)):
    stack = deque([(pos)])
    lowest_moves = math.inf
    visited = dict()
    visited[pos] = [pos]
    routes = []
    while len(stack) > 0:
        current_pos = stack.pop()
        if current_pos == Point(grid.width() - 1, grid.height() - 1):
            lowest_moves = min(lowest_moves, len(visited[current_pos]) - 1)
            routes.append(visited[current_pos])
            print(lowest_moves)
            print(visited[current_pos])

        next_moves = [n for n in grid.get_point_neighbours(current_pos) if grid.get(n) == '.' and n not in stack]
        for n in next_moves:
            if n in visited:
                if len(visited[n]) <= len(visited[current_pos]) + 1:
                    continue
            visited[n] = visited[current_pos] + [n]
            stack.append(n)
    grid.populate_points('O', visited[Point(grid.width() - 1, grid.height() - 1)])
    print(grid)
    return lowest_moves, routes


# part one = 404
# part two = 27,60
if __name__ == '__main__':

    day = 18
    expected1, expected2 = 22, Point(6,1)

    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')
    grid, _ = parse_input(test_input, 7, 7, 12)
    print(f'Test input: \n{grid}')

    # Test part 1
    test_result = part_one(grid)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    grid, points = parse_input(test_input, 7, 7, 12)
    # test_result2 = part_two(grid, points, 12)
    test_result2 = part_two2(test_input, 7, 7)
    print(f'Part 2 test: {test_result2}')
    assert test_result2 == expected2


    real_input = input.read_strings(day, year=2024, from_file=False)
    grid, _ = parse_input(real_input, 71, 71, 1024)
    print(f'Real input: \n{grid}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    real_result = part_one(grid)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')
    assert real_result == 404

    # Real part 2
    pre_dropped = 1024
    grid, points = parse_input(real_input, 71, 71, pre_dropped)
    print(f'Part 2 real input: \n{grid}')

    start = timer()
    # result2 = part_two(grid, points, pre_dropped)
    result22 = part_two2(real_input, 71, 71)
    print(f'Part 2: {result22}')
    print(f'Time: {timer() - start}')
    assert result22 == Point(27,60)


