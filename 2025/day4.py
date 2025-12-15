import input
from mytypes.grid import Grid


def part_one(grid: Grid):
    total = 0
    for cell, value in grid:
        if value != '@':
            continue
        adjacent = sum([1 if grid[neighbour] in ('@', 'x') else 0 for neighbour in grid.get_point_neighbours_inc_diag(cell)])
        if adjacent < 4:
            total += 1
            grid[cell] = 'x'

    print(f"Removed {total} boxes")
    # print(grid)
    for cell, value in grid:
        if value == 'x':
            grid[cell] = '.'
    return total


def part_two(grid: Grid):
    total = part_one(grid)
    grand_total = total
    while total > 0:
        total = part_one(grid)
        grand_total += total
    return grand_total

def parse_input(input_list):
    return input_list

# part one =
# part two =
if __name__ == '__main__':

    day = 4
    expected1, expected2 = 13, 43

    test_input = input.read_grid(day, year=2025, from_file=True, test=True)
    print(f'Test input: \n{test_input}')
    parsed_test_input = parse_input(test_input)
    print(f'Parsed test input: \n{parsed_test_input}')

    # Test part 1
    test_result = part_one(parsed_test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    test_input = input.read_grid(day, year=2025, from_file=True, test=True)
    print(f'Test input: \n{test_input}')
    parsed_test_input = parse_input(test_input)
    print(f'Parsed test input: \n{parsed_test_input}')

    test_result2 = part_two(parsed_test_input)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2

    # exit(0)

    real_input = input.read_grid(day, year=2025, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    parsed_real_input = parse_input(real_input)
    real_result = part_one(parsed_real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    real_input = input.read_grid(day, year=2025, from_file=False)
    parsed_real_input = parse_input(real_input)

    start = timer()
    result2 = part_two(parsed_real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
