import math

import input


def part_one(equations: list):
    total = 0
    for operation in equations:
        result = 0
        operands, operator = list(map(int, operation[:-1])), operation[-1]
        if operator == '+':
            result = sum(operands)
        else:
            result = math.prod(operands)
        total += result
        # print(f'Operands: {operands}, Operator: {operator}, Result: {result}')
    return total


def part_two(_input):
    width = max([len(row) for row in _input])
    operands = []
    operator = ''
    total = 0
    for col in range(width - 1, -1, -1):
        num, operator = '', None
        for row in range(len(_input)):
            if len(_input[row]) <= col:
                continue
            if _input[row][col] in ('+', '*'):
                operator = _input[row][col]
                break
            elif len(_input[row][col].strip()) > 0:
                num = num + _input[row][col]
        if len(num) == 0:
            continue
        operands.append(int(num))
        if operator is not None:
            if operator == '+':
                result = sum(operands)
            else:
                result = math.prod(operands)
            total += result
            print(f'Operands: {operands}, Operator: {operator}, Result: {result}')
            operands = []

    return total


def parse_input2(input_list):
    return [row.strip('\n') for row in input_list]


def parse_input(input_list):
    operands = []
    for line in input_list:
        operands.append(line.split())
    return list(zip(*operands))

# part one =
# part two =
if __name__ == '__main__':

    day = 6
    expected1, expected2 = 4277556, 3263827

    test_input = input.read_strings(day, year=2025, from_file=True, test=True, strip=False)
    print(f'Test input: \n{test_input}')
    parsed_test_input = parse_input(test_input)
    print(f'Parsed test input: \n{parsed_test_input}')

    # Test part 1
    test_result = part_one(parsed_test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    parsed_test_input2 = parse_input2(test_input)
    print(f'Parsed test input 2: \n{parsed_test_input2}')
    test_result2 = part_two(parsed_test_input2)
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
    real_result = part_one(parsed_real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    parsed_input2 = parse_input2(real_input)
    print(f'Parsed input 2: \n{parsed_input2}')
    start = timer()
    result2 = part_two(parsed_input2)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
