from numpy import bool_, int_, ndarray

import input
from mytypes.grid import Point3D, Point
import numpy as np


np.set_printoptions(edgeitems=50)
void, lava, air = 0, -1, 9


def part1(points: list[Point3D]):
    total = 0
    for p in points:
        sides = 6
        for q in points:
            if p == q:
                continue
            if p.distance(q) == 1:
                sides -= 1
        # print(f'{p} has {sides} open sides')
        total += sides

    return total


def get_unchecked_neighbours(grid, x, y, z):
    return get_neighbours(grid, x, y, z, void)


def get_external_neighbours(grid, x, y, z):
    return get_neighbours(grid, x, y, z, air)


def get_neighbours(grid, x, y, z, val: int):
    neighbours = {(x + 1, y, z), (x, y + 1, z), (x - 1, y, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)}
    return [(p[0], p[1], p[2]) for p in neighbours
            if 0 <= p[0] < grid.shape[2]
            and 0 <= p[1] < grid.shape[1]
            and 0 <= p[2] < grid.shape[0]
            and grid[p[2], p[1], p[0]] == val]


def parse_grid(points: list[Point3D]):
    max_x, max_y, max_z = max([p.x for p in points]), max([p.y for p in points]), max([p.z for p in points])
    grid = np.zeros(shape=(max_z + 3, max_y + 3, max_x + 3), dtype=int_)
    for p in points:
        grid[p.z, p.y, p.x] = lava
    print(grid)

    queue = [(0, 0, 0)]
    while queue:
        current = queue.pop(0)
        neighbours = get_unchecked_neighbours(grid, *current)
        for n in neighbours:
            grid[n[2], n[1], n[0]] = air
        queue.extend(neighbours)
    print(grid)
    print(f'Voids: {np.sum(grid == void)}')
    return grid


def get_surface_area(grid: ndarray, points: list[Point3D]):
    total = 0
    while points:
        p = points.pop()
        surfaces = len(get_external_neighbours(grid, p.x, p.y, p.z))
        grid[p.z, p.y, p.x] = surfaces
        total += surfaces
    print(grid)
    return total


if __name__ == '__main__':
    # cubes = input.read_strings(18, year=2022, from_file=True, filename='2022/day18test.txt')
    cubes = input.read_strings(18, year=2022)
    print(cubes)
    points = [Point3D(*cube.split(',')) + Point3D(1, 1, 1) for cube in cubes]
    print(points)

    # pt 1
    surface_area = part1(points)
    print(surface_area)

    # pt 2
    grid = parse_grid(points)
    surface_area = get_surface_area(grid, points)
    print(surface_area)
    print(grid[grid < 9])
    print(sum(grid[grid < 9]))


