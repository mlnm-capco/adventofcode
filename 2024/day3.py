import input
import re

PATTERN = r'mul\([0-9]*,[0-9]*\)'


def multiply(operation):
    match = re.match(r'mul\(([0-9]*),([0-9]*)\)', operation)
    return int(match.group(1)) * int(match.group(2))


def part_one(input: str):

    operations = re.findall(PATTERN, ''.join(input))
    print(operations)
    total = 0
    for op in operations:
        total += multiply(op)

    return total


def part_two(input):
    operations = re.findall(r'(mul|do|don\'t)\(([0-9]*),?([0-9]*)\)', ''.join(input))
    print(operations)

    enabled = True
    total = 0


    # for op in operations:
    #     match op[0]:
    #         case 'mul':
    #             if enabled:
    #                 print('enabled')


    for op in operations:
        if enabled and op[0] == 'mul':
            total += int(op[1]) * int(op[2])
        elif op[0] == 'do':
            enabled = True
        elif op[0] == 'don\'t':
            enabled = False
    return total


# part one = 192767529
# part two =
if __name__ == '__main__':

    input = input.read_strings(3, year=2024, from_file=False, filename='../input/2024/day3test.txt')

    print(f'Input: {input}')

    result = part_one(input)
    print(f'Part 1: {result}')

    result2 = part_two(input)
    print(f'Part 2: {result2}')


