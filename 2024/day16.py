import math
from collections import deque

import input
from mytypes.grid import Grid, Point, Direction


def part_one(grid: Grid):
    robot_pos = Point(1, grid.height() - 2)
    return solve_maze(grid, robot_pos)[0]


def solve_maze(grid: Grid, pos: Point):
    stack = deque([(pos, Direction.R, 0, {pos})])
    lowest_score = math.inf
    visited = dict()
    lowest_path = set()
    while len(stack) > 0:
        current_pos, direction, current_score, current_path = stack.pop()
        print(f'{len(stack)}, {current_pos}, {lowest_score}')
        if current_pos == Point(grid.width() - 2, 1):
            if lowest_score == current_score:
                lowest_path.update(current_path)
            elif current_score < lowest_score:
                lowest_path = set()
                lowest_path.update(current_path)
            lowest_score = min(lowest_score, current_score)
            continue

        if (current_pos, direction) in visited and current_score > visited[(current_pos, direction)]:
            continue
        # direction, current_score = d, 1000.
        # v=u, 5000
        better_path_found = False
        for v in Direction:
            if (current_pos, v) in visited and visited[(current_pos, v)] + ((v - direction) * 1000) < current_score:
                # existing path would be cheaper if it rotated to current direction
                better_path_found = True
                break

            # if (current_pos, v) in visited and current_score + ((v - direction) * 1000) > visited[(current_pos, v)] and current_score > visited[(current_pos, v)]:
            #     better_path_found = True
            #     break

        if better_path_found:
            continue

        next_moves = [n for n in grid.get_point_neighbours(current_pos) if grid.get(n) in '.E']
        for n in next_moves:
            new_direction = Direction.from_point(n - current_pos)
            turns = new_direction - direction
            new_score = current_score + 1 + (turns * 1000)
            stack.append((n, new_direction, new_score, current_path.union({n})))
        visited[(current_pos, direction)] = current_score
    return lowest_score, len(lowest_path)


def part_two(grid: Grid):
    robot_pos = Point(1, grid.height() - 2)
    return solve_maze(grid, robot_pos)[1]


# part one = 858038 too high
# part two =
if __name__ == '__main__':

    day = 16
    expected1, expected2 = 7036, 45

    test_input = input.read_grid(day, year=2024, from_file=True, as_ints=False, filename=f'../input/2024/day{day}test.txt')
    print(f'Test input: \n{test_input}')

    # Test part 1
    test_result = part_one(test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1


    # Test part 2
    test_result2 = part_two(test_input)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2


    real_input = input.read_grid(day, year=2024, as_ints=False, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    # start = timer()
    # real_result = part_one(real_input)
    # print(f'Part 1: {real_result}')
    # print(f'Time: {timer() - start}')



    # Real part 2
    start = timer()
    result2 = part_two(real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')


