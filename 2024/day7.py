import operator
from functools import reduce

import input


class Sum:

    @staticmethod
    def from_string(input: str):
        total, operands = input.split(':')
        return Sum(int(total), list(map(int, operands.strip().split())))

    def __init__(self, total: int, operands: list[int]):
        self.total = total
        self.operands = operands

    def __repr__(self):
        return f'\nTotal: {self.total}, Operands: {self.operands}, Solvable: {self.is_solvable()}'

    def is_solvable(self):
        if len(self.operands) == 2:
            return (sum(self.operands) == self.total
                    or self.operands[0] * self.operands[1] == self.total
            or int(str(self.operands[0]) + str(self.operands[1])) == self.total)
        return ((Sum(self.total, [self.operands[0] + self.operands[1], *self.operands[2:]]).is_solvable()
                or Sum(self.total, [self.operands[0] * self.operands[1], *self.operands[2:]]).is_solvable())
                or Sum(self.total, [int(str(self.operands[0]) + str(self.operands[1])), *self.operands[2:]]).is_solvable())


def part_one(input):
    return sum([s.total for s in sums if s.is_solvable()])


def part_two(input):
    return NotImplemented


# part one = 1298103531759
# part two =
if __name__ == '__main__':

    day, test = 7, False
    input = input.read_strings(day, year=2024, from_file=test, filename=f'../input/2024/day{day}test.txt')

    print(f'Input: {input}')
    sums = [Sum.from_string(i) for i in input]

    print(sums)

    result = part_one(sums)
    print(f'Part 1: {result}')

    result2 = part_two(input)
    print(f'Part 2: {result2}')


