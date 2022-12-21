import input
from functools import cmp_to_key


def compare(op1, op2):
    if type(op1) == int and type(op2) == int:
        return op2 - op1
    if type(op1) == list and type(op2) == list:
        for i in range(0, max(len(op1), len(op2))):
            if i >= len(op1):
                return 1
            elif i >= len(op2):
                return -1
            else:
                res = compare(op1[i], op2[i])
                if res != 0:
                    return res
        return 0
    elif type(op1) == int:
        return compare([op1], op2)
    else:
        return compare(op1, [op2])


def part_1():
    total = 0
    for i in range(0, len(pairs) - 1, 3):
        result = compare(eval(pairs[i]), eval(pairs[i + 1]))
        if result > 0:
            print(int(i / 3) + 1)
            total += (int(i / 3) + 1)
    print(total)
    return total


def part_2():
    all_pairs = [eval(pair) for pair in pairs if len(pair) > 0]
    all_pairs.append([[6]])
    all_pairs.append([[2]])
    print(all_pairs)
    all_pairs = sorted(all_pairs, key=cmp_to_key(compare), reverse=True)
    print('Sorted:')
    print(*all_pairs, sep='\n')
    index_of_two = all_pairs.index([[2]]) + 1
    index_of_six = all_pairs.index([[6]]) + 1
    print(f'[[2]] at index {index_of_two} [[6]] at index {index_of_six}')
    return index_of_two * index_of_six


if __name__ == '__main__':
    # pairs = input.read_strings(13, year=2022, from_file=True, filename='2022/day13test.txt')
    pairs = input.read_strings(13, year=2022)
    print(pairs)

    print(part_2())


