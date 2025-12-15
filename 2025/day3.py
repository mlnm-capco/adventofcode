import input


def part_one(_input):
    total = 0
    for bank in _input:
        max1, max2 = -1, -1
        for battery in bank[:-1]:
            if int(battery) > max1:
                max1 = int(battery)
                max2 = -1
            elif max1 > -1 and int(battery) > max2:
                max2 = int(battery)
        max2 = max(max2, int(bank[-1:]))
        result = ''.join([str(max1), str(max2)])
        # print(f'{result}')
        total += int(result)
    return total


def part_two(_input, length=12):
    total = 0
    for bank in _input:
        idxi, batteries = -1, []
        for i in range(length):
            start, end = idxi + 1, (i - length) % len(bank) + 1
            maxi = max(bank[start: end])
            idxi = bank.index(maxi, start, end)
            batteries.append(str(maxi))
        result = ''.join(batteries)
        # print(f'{result}')
        total += int(result)
    return total


def parse_input(input_list):
    return input_list

# part one = 17330
# part two = 171518260283767
if __name__ == '__main__':

    day = 3
    expected1, expected2 = 357, 3121910778619

    test_input = input.read_strings(day, year=2025, from_file=True, test=True)
    print(f'Test input: \n{test_input}')
    parsed_test_input = parse_input(test_input)
    print(f'Parsed test input: \n{parsed_test_input}')

    # Test part 1
    # test_result = part_one(parsed_test_input)
    test_result = part_two(parsed_test_input, length=2)
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
    # real_result = part_one(parsed_real_input)
    real_result = part_two(parsed_real_input, length=2)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(parsed_real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')

