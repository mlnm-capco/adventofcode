from collections import deque

import input
from mytypes.grid import Grid, Point, Direction


def part_one(_grid: Grid):
    total = 0
    visited = set()
    for j in range(0, _grid.height()):
        for i in range(0, _grid.width()):
            p = Point(i, j)
            if p not in visited:
                total += calculate_plot_fence(_grid, p, visited)
    return total


def calculate_plot_fence(_grid: Grid, start_point: Point, visited: set[Point]):
    plot = _grid.get(start_point)
    stack = deque([start_point])
    area, perimeter = 0, 0
    while len(stack) > 0:
        current_location = stack.pop()
        visited.add(current_location)
        neighbours = [n for n in _grid.get_point_neighbours(current_location) if _grid.get(n) == plot]
        perimeter += (4 - len(neighbours))
        area += 1
        # print(f'Point {current_location}: neighbours: {len(neighbours)}, perimeter {4 - len(neighbours)}')
        unvisited_neighbours = [n for n in neighbours if n not in visited and n not in stack]
        stack.extend(unvisited_neighbours)
    # print(f'Cost of plot {plot}: area {area} * perimiter {perimeter} = {area * perimeter}')
    return area * perimeter


##### Part 2

def part_two(_grid: Grid):
    total = 0
    visited = set()
    for j in range(0, _grid.height()):
        for i in range(0, _grid.width()):
            p = Point(i, j)
            if p not in visited:
                total += calculate_plot_fence2(_grid, p, visited)
    return total


def calculate_plot_fence2(_grid: Grid, start_point: Point, visited: set[Point]):
    plot = _grid.get(start_point)
    stack = deque([start_point])
    area, perimeter = 0, 0
    plot_map = set()
    while len(stack) > 0:
        area += 1
        current_location = stack.pop()
        plot_map.add(current_location)
        visited.add(current_location)
        neighbours = [n for n in _grid.get_point_neighbours(current_location) if _grid.get(n) == plot and n not in visited and n not in stack]
        # print(f'Point {current_location}: neighbours: {len(neighbours)}, perimeter {4 - len(neighbours)}')
        stack.extend(neighbours)
    # print(f'Cost of plot {plot}: area {area} * perimiter {perimeter} = {area * perimeter}')
    perimeter = count_sides(_grid, plot_map, plot)
    return area * perimeter


def count_sides(_grid: Grid, plot_map: set, plot: str):
    # print(f'Counting sides of {plot_map}')
    sides: set[tuple[Point, Point, Direction]] = set()
    for point in plot_map:
        neighbours = [n for n in _grid.get_point_neighbours(point) if _grid.get(n) != plot]
        for n in neighbours:
            sides.add((point, point, Direction.from_point(n - point)))
        if point.x == 0:
            sides.add((point, point, Direction.L))
        if point.y == 0:
            sides.add((point, point, Direction.U))
        if point.x == _grid.width() - 1:
            sides.add((point, point, Direction.R))
        if point.y == _grid.height() - 1:
            sides.add((point, point, Direction.D))
    return len(join_sides(sides))

def join_sides(sides: set[tuple[Point, Point, Direction]]):
    while do_join(sides):
        # print(f'Joining {sides}')
        continue
    return sides


def do_join(sides):
    for side1 in sides:
        for side2 in sides:
            if side1 == side2 or side1[2] != side2[2]:
                continue
            start1, end1, orientation = side1
            start2, end2, _ = side2
            if (((orientation == Direction.U or orientation == Direction.D) and start1.y == start2.y and (
                    abs(start1.x - end2.x) == 1 or abs(end1.x - start2.x)) == 1)
                    or ((orientation == Direction.L or orientation == Direction.R) and start1.x == start2.x and (
                            abs(start1.y - end2.y) == 1 or abs(end1.y - start2.y) == 1))):
                new_start = Point(min(start1.x, start2.x), min(start1.y, start2.y))
                new_end = Point(max(end1.x, end2.x), max(end1.y, end2.y))
                new_side = (new_start, new_end, orientation)
                # print(f'Joined sides {side1} + {side2} = {new_side}')
                sides.remove(side1)
                sides.remove(side2)
                sides.add(new_side)
                return True
    return False


# part one = 1450422
# part two =
if __name__ == '__main__':

    day, test = 12, True
    test_input = input.read_grid(day, year=2024, from_file=test, as_ints=False, filename=f'../input/2024/day{day}test.txt')
    print(f'Test Input: \n{test_input}')

    test_result = part_one(test_input)
    print(f'Part 1 test: {test_result}')
    assert test_result == 1930

    test_result2 = part_two(test_input)
    print(f'Part 2 test: {test_result2}')
    assert test_result2 == 1206

    real_input = input.read_grid(day, year=2024, from_file=False, as_ints=False)
    print(f'Input: \n{real_input}')

    from timeit import default_timer as timer

    start = timer()
    result = part_one(real_input)
    print(f'Part 1: {result}')
    print(timer() - start)
    assert result == 1450422

    start = timer()
    result2 = part_two(real_input)
    print(f'Part 2: {result2}')
    print(timer() - start)
    assert result2 == 906606



