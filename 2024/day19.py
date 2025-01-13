import regex
import input


def part_one(towels, designs):
    return sum(regex.fullmatch(f'({towels})*', d) is not None for d in designs)


def part_two(towels, designs):
    t_list = towels.split('|')
    total = 0
    cache = dict()
    for design in designs:
        combos = count_combos(design, t_list, cache)
        total += combos
        print(f'Design: {design} combos: {combos}, cache: {len(cache)}')

    return total

def count_combos(design, t_list, cache):
    total = 0
    if design in cache:
        return cache[design]
    if regex.fullmatch(f'({"|".join(t_list)})*', design) is None:
        cache[design] = 0
        return 0
    for t in t_list:
        if t == design:
            total += 1
        elif regex.match(f'^{t}.*', design):
            total += count_combos(design[len(t):], t_list, cache)
    cache[design] = total
    return total

def parse_input(input):
    towels = '|'.join(input[0].split(', '))
    designs = [line for line in input[2:]]
    return towels, designs

# part one =
# part two =
if __name__ == '__main__':

    day = 19
    expected1, expected2 = 6, 16

    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')
    towels, designs = parse_input(test_input)
    print(f'Test input: \n{towels, designs}')

    # Test part 1
    test_result = part_one(towels, designs)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    test_result2 = part_two(towels, designs)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2

    real_input = input.read_strings(day, year=2024, from_file=False)
    towels, designs = parse_input(real_input)
    print(f'Real input: \n{towels, designs}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    real_result = part_one(towels, designs)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')
    assert real_result == 240

    # Real part 2
    start = timer()
    result2 = part_two(towels, designs)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
    assert result2 == 848076019766013


