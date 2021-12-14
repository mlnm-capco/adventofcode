import math
import input
from collections import deque
from mytypes.vent import Point
import timeit


def is_trough(grid, x, y):
    return next(filter(lambda p: grid[y][x] >= grid[p.y][p.x], get_neighbours(grid, x, y)), None) is None


def get_troughs(grid):
    points = []
    for y in range(0, len(grid)):
        points.extend([Point(x, y) for x in range(0, len(grid[0])) if is_trough(grid, x, y)])
    return points


def get_neighbours(grid, x, y):
    neighbours = {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}
    return [Point(p[0], p[1]) for p in neighbours if 0 <= p[0] < len(grid[0]) and 0 <= p[1] < len(grid)]


def get_basins(troughs):
    return [get_basin(trough) for trough in troughs]


def get_basin(trough: Point):
    stack = deque([trough])
    visited = set()
    while len(stack) > 0:
        current = stack.pop()
        visited.add(current)
        neighbours = [p for p in get_neighbours(grid, current.x, current.y)
                      if p not in visited and grid[current.y][current.x] <= grid[p.y][p.x] < 9]
        stack.extend(neighbours)
    return len(visited)


def part1(grid):
    return sum([grid[point.y][point.x] + 1 for point in get_troughs(grid)])


def part2(grid):
    basins = sorted(get_basins(get_troughs(grid)), reverse=True)
    return math.prod(basins[:3])


if __name__ == '__main__':
    grid = input.read_grid()
    print(part1(grid))  # 572
    print(part2(grid))
   #  print(part2(grid))  # 847044

