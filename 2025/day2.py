import sympy

import input
from sympy import isprime
import math

def part_one(_input):
    total = 0
    for start, end in _input:
        for i in range(int(start), int(end) + 1):
            if len(str(i)) % 2 == 1:
                continue
            n = len(str(i)) // 2
            if str(i)[:n] == str(i)[-n:]:
                total += i
    return total


def find_factors(num):
    factors = []
    for i in range(1, int(math.sqrt(num)) + 1):
        if num % i == 0:
            factors.append(i)
            if i != num // i and i != 1:
                factors.append(num // i)
    return sorted(factors)


def part_two(_input):
    total, result, results = 0, False, set()
    for start, end in _input:
        for i in range(int(start), int(end) + 1):
            length = len(str(i))
            if length < 2:
                continue
            for factor in find_factors(length):
                result = True
                first_n = str(i)[:factor]
                for j in range(1, length // factor):
                    if str(i)[j * factor: (j * factor) + factor] != first_n:
                        result = False
                        break
                if result and i not in results:
                    print(f'Number {i} is made of repeated segment {first_n} of length {factor}')
                    total += i
                    results.add(i)
    return total


def parse_input(input_list):
    return [tuple(range.split('-')) for range in input_list]

# part one = 23039913998
# part two = 35950619190 too high
if __name__ == '__main__':

    day = 2
    expected1, expected2 = 1227775554, 4174379265

    test_input = input.read_csv_strings(day, year=2025, from_file=True, test=True)
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

    real_input = input.read_csv_strings(day, year=2025, from_file=False)
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
