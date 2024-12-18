from time import sleep

import regex

import input
from mytypes.grid import Point, Grid


def part_one(input, width: int = 11, height: int = 7):
    robots = parse_input(input)
    grid = Grid.fill(0, width, height)
    moves = 100
    moved_robots = []
    for robot_location, robot_move in robots:
        new_location = robot_location + (robot_move * moves)
        new_location = grid.normalise(new_location)
        grid[new_location.y][new_location.x] += 1
        moved_robots.append((new_location, robot_move))
    print(grid)
    quadrant1 = sum([sum(r[0:int(grid.width() / 2)]) for r  in grid[0:int(grid.height() / 2)]])
    quadrant2 = sum([sum(r[0:int(grid.width() / 2)]) for r  in grid[int(grid.height() / 2) + 1:]])
    quadrant3 = sum([sum(r[int(grid.width() / 2)+ 1:]) for r  in grid[0:int(grid.height() / 2)]])
    quadrant4 = sum([sum(r[int(grid.width() / 2) + 1:]) for r  in grid[int(grid.height() / 2) + 1:]])
    result = quadrant1 * quadrant2 * quadrant3 * quadrant4
    print(f'{quadrant1, quadrant2, quadrant3, quadrant4} = {result}')
    return result


def part_two(input, width: int = 11, height: int = 7):
    robots = parse_input(input)
    grid = Grid.fill(0, width, height)
    for robot_location, robot_move in robots:
        grid[robot_location.y][robot_location.x] += 1
    best_likeness, best_index = int(height / 2), 0
    for i in range(0, 100000):
        likeliness = assert_xmas_tree(grid)
        if likeliness > best_likeness:
            print(f'\n{i}*******:\n{grid}')
            best_likeness, best_index = likeliness, i
        if is_symmetrical(grid):
            print(f'\n{i}*******:\n{grid}\n ************ Symmetrical ****************')
            return i

        # sleep(1)
        moved_robots = []
        for robot_location, robot_move in robots:
            new_location = robot_location + (robot_move)
            new_location = grid.normalise(new_location)
            grid[robot_location.y][robot_location.x] -= 1
            grid[new_location.y][new_location.x] += 1
            moved_robots.append((new_location, robot_move))
        robots = moved_robots
    return best_index

def assert_xmas_tree(grid: Grid):
    current_size = 0
    increasing = 0
    for row in grid:
        for e in row:
            if e > 1:
                return 0
    return 10000000
    #     size = sum(row)
    #     if size >= current_size:
    #         increasing += 1
    #         current_size = size
    # return increasing

def is_symmetrical(grid: Grid):
    for row in grid:
        if row[0: int(len(row)/2)] != row[int(len(row)/2) + 1:]:
            return False
    return True

def parse_input(_input: list[str]):
    robots = [parse_robot(line) for line in _input]
    print(robots)
    return robots


# p=9,5 v=-3,-3
def parse_robot(line):
    match = regex.match('p=(-?[0-9]*),(-?[0-9]*) v=(-?[0-9]*),(-?[0-9]*)', line)
    return Point(match.group(1), match.group(2)), Point(match.group(3), match.group(4))


# part one = 236628054
# part two = 500 too low, 100000 too high
if __name__ == '__main__':

    day = 14
    expected1, expected2 = 12, -1

    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')
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

    # exit(0)

    real_input = input.read_strings(day, year=2024, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    real_result = part_one(real_input, 101, 103)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')
    assert real_result == 236628054

    # Real part 2
    start = timer()
    result2 = part_two(real_input, 101, 103)
    print(f'Part2: {result2}')
    print(f'Time: {timer() - start}')


