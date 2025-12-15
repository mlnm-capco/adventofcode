import input
from mytypes.grid import parse_grid, Grid


def part_one(grid: Grid):
    streams = set()
    total = 0
    streams.add(grid[0].index("S"))
    for i in range(len(grid)):
        new_streams = streams.copy()
        for s in streams:
            if grid[i][s] == '^':
                total += 1
                new_streams.remove(s)
                new_streams.add(s - 1)
                new_streams.add(s + 1)
        streams = new_streams
    return total


def part_two(grid: Grid):
    timelines = {grid[0].index("S"): 1}
    for row in range(1, len(grid)):
        next_timelines = {}
        for timeline in timelines:
            current = timelines[timeline]
            if grid[row][timeline] == '^':
                next_timelines[timeline - 1] = current + next_timelines.get(timeline - 1, 0)
                next_timelines[timeline + 1] = current + next_timelines.get(timeline + 1, 0)
            else:
                next_timelines[timeline] = next_timelines.get(timeline, 0) + timelines[timeline]
            grid[row - 1][timeline] = str(current)
        timelines = next_timelines

    print(f'{grid}')
    return sum(timelines.values())


def parse_input(input_list):
    return Grid(input_list, False)

# part one = 1524
# part two = 32982105837605
if __name__ == '__main__':

    day = 7
    expected1, expected2 = 21, 40

    test_input = input.read_strings(day, year=2025, from_file=True, test=True)
    print(f'Test input: \n{test_input}')
    parsed_test_input = parse_input(test_input)
    print(f'Parsed test input: \n{parsed_test_input}')

    # Test part 1
    test_result = part_one(parsed_test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    test_result2 = part_two(parsed_test_input)
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
    print(f'Parsed real input: \n{parsed_real_input}')

    real_result = part_one(parsed_real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(parsed_real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
