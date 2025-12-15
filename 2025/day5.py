import input


def part_one(ranges, ingredients):
    print(f'Ranges: {ranges}')
    print(f'Ingredients: {ingredients}')
    fresh = 0
    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                print(f'Ingredient {ingredient} is in range {r}')
                fresh += 1
                break
        else:
            print(f'Ingredient {ingredient} is spoiled')
    return fresh


def part_two(ranges):
    squashed_ranges = set()
    for range in ranges:
        squashed_ranges.add(range)
        overlaps = set()
        for squashed in squashed_ranges:
            if not (range[1] < squashed[0] or range[0] > squashed[1]):
                overlaps.add(squashed)
        min_start, max_end = min(r[0] for r in overlaps), max(r[1] for r in overlaps)
        for overlap in overlaps:
            squashed_ranges.remove(overlap)
        squashed_ranges.add((min_start, max_end))

    print(f'Squashed ranges: {squashed_ranges}')
    return sum(r[1] - r[0] + 1 for r in squashed_ranges)


def parse_input(input_list):
    ranges, ingredients = [], []
    for line in input_list:
        if '-' in line:
            ranges.append(tuple(map(int, line.split('-'))))
        elif len(line.strip()) > 0:
            ingredients.append(int(line))
    print(f'Ranges" {len(ranges)}, ingredients: {len(ingredients)}')
    return ranges, ingredients

# part one = 180 too low
# part two =
if __name__ == '__main__':

    day = 5
    expected1, expected2 = 3, 14

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
    test_result2 = part_two(parsed_test_input[0])
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
    result2 = part_two(parsed_real_input[0])
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
