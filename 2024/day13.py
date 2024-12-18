import math
from math import gcd

from regex import regex

import input


# Machine for (as it turns out) solving simultaneous equations (and also diophantic equations - naively)
class Machine:

    def __init__(self, ax, ay, bx, by, prize_x, prize_y, extra:int = 0):
        self.ax, self.ay, self.bx, self.by, self.prize_x, self.prize_y = ax, ay, bx, by, prize_x + extra, prize_y + extra

    def __repr__(self):
        return f'A: {self.ax, self.ay}, B: {self.bx, self.by}, Prize: {self.prize_x, self.prize_y}'

    # A: ('94', '34'), B: ('22', '67'), Prize: ('8400', '5400')
    def solve_diophantine(self, max_presses:int = 100):
        gcd_x = gcd(self.ax, self.bx)
        gcd_y = gcd(self.ay, self.by)
        if self.prize_x % gcd_x != 0 or self.prize_y % gcd_y != 0:
            print(f'No solution for {self}')
            return []

        if self.prize_x % self.bx == 0 and self.prize_y % self.by == 0 and self.prize_x / self.bx == self.prize_y / self.by:
            return [(0, int(self.prize_x / self.bx))]
        self.ax, self.bx, self.prize_x = int(self.ax / gcd_x), int(self.bx / gcd_x), int(self.prize_x / gcd_x)
        self.ay, self.by, self.prize_y = int(self.ay / gcd_y), int(self.by / gcd_y), int(self.prize_y / gcd_y)

        results = []
        for a_presses in range(0, max_presses + 1):
            if (self.prize_x - (a_presses * self.ax)) % self.bx == 0:
                b_presses = int((self.prize_x - (a_presses * self.ax)) / self.bx)
                # possible result, now check it fits y
                if a_presses * self.ay + b_presses * self.by == self.prize_y:
                    # bingo
                    results.append((a_presses, b_presses))
        print(f'Found result {results} for machine {self}')
        return results

    # A: ('94', '34'), B: ('22', '67'), Prize: ('8400', '5400')
    # X: 94a + 22b = 8400
    # Y: 34a + 67b = 5400
    def solve_simultaneously(self):
        gcd_x = gcd(self.ax, self.bx)
        gcd_y = gcd(self.ay, self.by)

        if self.prize_x % gcd_x != 0 or self.prize_y % gcd_y != 0:
            # print(f'No solution for {self}')
            return None

        # multiply everything in x equation by ay
        new_ax, new_bx, new_prize_x = self.ax * self.ay, self.bx * self.ay, self.prize_x * self.ay
        # multiply everything in y equation by ax
        new_ay, new_by, new_prize_y = self.ay * self.ax, self.by * self.ax, self.prize_y * self.ax
        # new_ax and new_ay cancel out, new_bx - new_by = new_prize_x - new_prize_y
        if (new_prize_x - new_prize_y) % (new_bx - new_by) != 0:
            # print(f'No integer solution for {self}')
            return None
        b = int((new_prize_x - new_prize_y) / (new_bx - new_by))
        a = int((self.prize_x - (self.bx * b)) / self.ax)
        assert a * self.ax + b * self.bx == self.prize_x
        assert a * self.ay + b * self.by == self.prize_y
        return (a, b)

        # print(f'Found result {results} for machine {self}')
        return results

def parse_input(lines: list[str], extra:int = 0):
    i = 0
    machines = []
    while i < len(lines):
        matcha = regex.match('Button A: X\+([0-9]*), Y\+([0-9]*)', lines[i])
        matchb = regex.match('Button B: X\+([0-9]*), Y\+([0-9]*)', lines[i + 1])
        matchprize = regex.match('Prize: X=([0-9]*), Y=([0-9]*)', lines[i + 2])
        ax, ay = int(matcha.group(1)), int(matcha.group(2))
        bx, by = int(matchb.group(1)), int(matchb.group(2))
        prize_x, prize_y = int(matchprize.group(1)), int(matchprize.group(2))
        machines.append(Machine(ax, ay, bx, by, prize_x, prize_y, extra))
        i += 4
    return machines

def part_one(_input: list[str]):

    _machines = parse_input(_input)
    print(_machines)

    total = get_minimum_cost(_machines)
    return total


def get_minimum_cost(_machines):
    total = 0
    for m in _machines:
        result = m.solve_simultaneously()
        if result is not None:
            total +=  result[0] * 3 + result[1]
    return total


def part_two(_input):

    _machines = parse_input(_input, 10000000000000)
    print(_machines)

    total = get_minimum_cost(_machines)
    return total

# part one = 36838
# part two = 83029436920891
if __name__ == '__main__':

    day = 13
    expected1, expected2 = 480, -1

    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')
    print(f'Test input: \n{test_input}')

    # Test part 1
    test_result = part_one(test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    test_result2 = part_two(test_input)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2


    real_input = input.read_strings(day, year=2024, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1

    start = timer()
    real_result = part_one(real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')
    assert real_result == 36838

    # Real part 2
    start = timer()
    result2 = part_two(real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')


