import input
from mytypes.grid import Grid
import numpy as np


def solve_grid(grid: Grid, results: list, x: int = 0, y: int = 0, total: int = 0):
    for i in range(0, 8):  # yuck
        for y in range(len(grid) - 1, -1, -1):
            for x in range(grid.width() - 1, -1, -1):
                if x == grid.width() - 1 and y == grid.height() - 1:
                    results[y][x] = grid[y][x]
                    continue
                neighbours = [n for n in grid.get_all_neighbours(x, y) if results[n.y][n.x] >= 0]
                neighbour_min = min([results[n.y][n.x] for n in neighbours]) if len(neighbours) > 0 else 0
                results[y][x] = grid[y][x] + neighbour_min
        print(f'{i}: {results[0][0]}')

    return results


def expand_grid(grid):
    np_grid = np.array(grid)
    new_grid = np_grid.copy()
    for i in range(1, 5):
        new_grid = np.concatenate([new_grid, (np_grid - 1 + i) % 9 + 1], axis=1)
    long_grid = new_grid.copy()
    for i in range(1, 5):
        new_grid = np.concatenate([new_grid, (long_grid - 1 + i) % 9 + 1], axis=0)
    return new_grid


if __name__ == '__main__':
    grid = input.read_grid(15, False, 'day15test1.txt')
    print(grid.width(), grid.height())
    print(grid)
    results = [[-1] * len(grid[0]) for _ in range(len(grid))]
    results = solve_grid(grid, results, len(grid[0]) - 1, len(grid) - 1)
    print(results)
    print(f'Answer (part 1): {results[0][0] - grid[0][0]}')

    expanded_grid = grid.expand_grid()
    print(f'Grid size: {expanded_grid.height(), expanded_grid.width()}')
    print(expanded_grid)
    results = [[-1] * expanded_grid.width() for _ in range(expanded_grid.height())]
    solve_grid(expanded_grid, results, expanded_grid.width() - 1, expanded_grid.height() - 1)
    print(results)
    print(f'Answer (part 2): {results[0][0] - grid[0][0]}')

    # pt2 = 2897