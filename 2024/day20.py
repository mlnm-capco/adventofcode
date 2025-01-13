from collections import deque

import input
from mytypes.grid import Grid, Point


def part_one(grid: Grid, threshold: int = 100):
    start = grid.find('S')
    solve_grid(grid)
    print(f'\n{grid}')
    print(f'Distance without shortcuts: {grid.get(start)}')
    shortcuts = calculate_shortcuts(grid)
    print(f'Shortcuts: {shortcuts}')
    return sum(s >= threshold for s in shortcuts.values())


def solve_grid(grid):
    start, end = grid.find('S'), grid.find('E')
    stack = deque([end])
    grid[end] = 0
    visited = {end}
    while len(stack) > 0:
        current_point = stack.pop()
        current_score = grid[current_point]
        if current_point == start:
            continue
        neighbours = [n for n in grid.get_point_neighbours(current_point) if n not in visited and grid.get(n) != '#']
        for n in neighbours:
            if isinstance(grid[n], int) and grid[n] < current_score + 1:
                continue
            grid[n] = current_score + 1
            stack.append(n)
        visited.add(current_point)
    return grid


def calculate_shortcuts(grid: Grid):
    shortcuts = dict()
    shortcuts_by_length = dict()
    for j in range(1, grid.height() - 1):
        for i in range(1, grid.width() - 1):
            if grid[j][i] == '#':
                shortcut = 0
                if isinstance(grid[j-1][i], int) and isinstance(grid[j+1][i], int):
                    shortcut = abs(grid[j-1][i] - grid[j+1][i]) - 2
                if isinstance(grid[j][i-1], int) and isinstance(grid[j][i+1], int):
                    shortcut = max(shortcut, abs(grid[j][i-1] - grid[j][i+1]) - 2)
                if shortcut > 0:
                    shortcuts[Point(i, j)] = shortcut
                    val = shortcuts_by_length.setdefault(shortcut, 0)
                    shortcuts_by_length[shortcut] = val + 1
    print(shortcuts_by_length)
    return shortcuts

def calculate_shortcuts_for_point(grid: Grid, start: Point, shortcuts: dict, max_picos = 20, threshold = 100):
    start_value = grid[start]
    stack = deque([start])
    visited = {start}
    distances = {start: 0}
    while len(stack) > 0:
        current_point = stack.popleft()
        picos = distances[current_point]
        neighbours = [n for n in grid.get_point_neighbours(current_point) if n not in visited and n not in stack and n != start]
        for n in neighbours:
            if grid[n] != '#' and picos > 0:
                if start_value > grid[n]:
                    shortcut_size = abs(start_value - grid[n]) - (picos + 1)
                    if shortcut_size >= threshold:
                        val = shortcuts.setdefault((start, n), 0)
                        shortcuts[(start, n)] = max(val, shortcut_size)
            if picos < max_picos - 1 and (n not in distances or distances[n] > picos):
                stack.append(n)
                distances[n] = picos + 1
        visited.add(current_point)
    return shortcuts

def part_two(grid: Grid, threshold = 50, debug = False):
    start = grid.find('S')
    solve_grid(grid)
    print(f'\n{grid}')
    print(f'Distance without shortcuts: {grid.get(start)}')
    shortcuts = dict()
    current_row = 0
    for p, value in grid:
        if value != '#':
            if p.y > current_row and p.y % 10 == 1:
                print(f'Processing row {p.y}: {value}')
                current_row = p.y
            calculate_shortcuts_for_point(grid, p, shortcuts, 20, threshold)
    print(f'Shortcuts: {shortcuts}')
    print(f'Number of shortcuts over threshold: {len(shortcuts)}')

    if debug:
        shortcuts_by_picos = dict()
        for v in shortcuts.values():
            shortcuts_by_picos[v] = sum(v1 == v for v1 in shortcuts.values())
        print([k for k, v in shortcuts.items() if v == 74])
        sorted_results = dict(sorted(shortcuts_by_picos.items()))
        print(sorted_results)
        assert sorted_results == {50: 32, 52: 31, 54: 29, 56: 39, 58: 25, 60: 23, 62: 20, 64: 19, 66: 12, 68: 14, 70: 12, 72: 22, 74: 4, 76: 3}

    return len(shortcuts)


# part one = 1404
# part two = 1141785 too high
if __name__ == '__main__':

    day = 20
    expected1, expected2 = 10, 285

    test_input = input.read_grid(day, year=2024, from_file=True, as_ints=False, filename=f'../input/2024/day{day}test.txt')
    print(f'Test input: \n{test_input}')

    # Test part 1
    test_result = part_one(test_input, 10)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    test_input = input.read_grid(day, year=2024, from_file=True, as_ints=False, filename=f'../input/2024/day{day}test.txt')
    test_result2 = part_two(test_input, 50, True)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2

    real_input = input.read_grid(day, year=2024, as_ints=False, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    real_result = part_one(real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')
    assert real_result == 1404

    # Real part 2
    real_input = input.read_grid(day, year=2024, as_ints=False, from_file=False)

    start = timer()
    result2 = part_two(real_input, 100)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')


