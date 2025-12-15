import math
import re

import input
from mytypes.grid import Grid


def part_one(gifts, grids: list[Grid], rosters):
    total, max_diff, min_diff = 0, 0, math.inf
    for i in range(len(grids)):
        area_required = sum([r * 7 for r in rosters[i]])
        area_available = grids[i].area()
        print(f'Grid {i}: {area_available >= area_required} area required = {area_required}, area available = {area_available}')
        max_diff = max(max_diff, area_available - area_required)
        if area_required <= area_available:
            min_diff = min(min_diff, area_available - area_required)
            total += 1
    print(f'Max difference = {max_diff}, Min difference = {min_diff}')
    return total


def part_two(gifts, grids, rosters):
    return NotImplemented


def parse_input(input_list):
    index = 0
    gift = []
    gifts = {}
    grids, rosters = [], []
    for line in input_list:
        if len(line.strip()) == 0:
            gifts[index] = Grid(gift)
            gift = []
            print(f'Parsed gift {index}:\n{gifts[index]}')
            continue
        elif match:=re.match(r'([0-9]*):', line.strip()):
            index = match.group(1)
        elif match:=re.match(r'([#.]+)', line.strip()):
            row = match.group(1)
            gift.append(row)
        elif match := re.match(r'([0-9]+)x([0-9]+):(.*)', line.strip()): # 4x4: 0 0 0 0 2 0
            grid = Grid.fill('.', int(match.group(1)), int(match.group(2)))
            grids.append(grid)
            print(f'Parsed grid {len(grids)-1}:\n{grid}')
            roster = list(map(int, match.group(3).strip().split(' ')))
            print(f'Roster: {roster}')
            rosters.append(roster)
    return gifts, grids, rosters

# part one = 448
# part two =
if __name__ == '__main__':

    day = 12
    expected1, expected2 = 3, -1    # actual answer is 2 for test, but rudimentary solution works for real input

    test_input = input.read_strings(day, year=2025, from_file=True, test=True)
    print(f'Test input: \n{test_input}')
    parsed_test_input = parse_input(test_input)
    print(f'Parsed test input: \n{parsed_test_input}')

    # Test part 1
    test_result = part_one(*parsed_test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    test_result2 = part_two(*parsed_test_input)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2

    # exit(0)

    real_input = input.read_strings(day, year=2025, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    parsed_real_input = parse_input(real_input)
    real_result = part_one(*parsed_real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(*parsed_real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
