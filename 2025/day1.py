import input


def part_one(_input):
    pos = 50
    zeroes = 0
    for turn in _input:
        clicks = turn[1] if turn[0] == 'R' else -turn[1]
        pos = (pos + clicks) % 100
        if pos == 0:
            zeroes += 1

    return zeroes


def part_two(_input):
    pos = 50
    zeroes = 0
    for turn in _input:
        clicks = turn[1] if turn[0] == 'R' else -turn[1]
        full_rotations, remainder = divmod(abs(clicks), 100)
        remainder = -remainder if turn[0] == 'L' else remainder
        new_pos = (pos + clicks) % 100
        rotations = full_rotations + (1 if ((pos + remainder <= 0 or pos + remainder >= 100) and pos != 0) else 0)
        if clicks > 99:
            print(f'Pos: {pos}, clicks={clicks}, new_pos={(pos + clicks) % 100} full_rotations={full_rotations}, remainder={remainder}, pos+remainder={pos+clicks}, rotations={rotations}')
        zeroes += rotations
        pos = new_pos


    return zeroes


def parse_input(input_list):
    return [ (s[0], int(s[1:])) for s in input_list ]

# part one = 1007
# part two = 5820
if __name__ == '__main__':

    day = 1
    expected1, expected2 = 3, 6

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

    real_input = input.read_strings(day, year=2025, from_file=True)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    parsed_real_input = parse_input(real_input)
    real_result = part_one(parsed_real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(parsed_real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')

    # Direct test for sample input
    sample_input = ['L68', 'L30', 'R48', 'L5', 'R60', 'L55', 'L1', 'L99', 'R14', 'L82']
    print(f'Sample input: {sample_input}')
    print(f'Parsed sample input: {parse_input(sample_input)}')
