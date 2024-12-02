import input
import re


def calculate_total_diff(list1, list2):
    return sum([abs(pair[0] - pair[1]) for pair in zip(sorted(list(map(int, list1))), sorted(list(map(int, list2))))])


def part_two(list1, list2):
    total = 0
    for val1 in list1:
        count = list2.count(val1)
        total += val1 * count
    return total


# part one = 2815556
# part two = 23927637
if __name__ == '__main__':

    list1, list2 = input.read_columns_as_int_lists(1, year=2024)

    print(f'List 1: {list1}')
    print(f'List 2: {list2}')

    result = calculate_total_diff(list1, list2)
    print(result)

    part2 = part_two(list1, list2)
    print(part2)
