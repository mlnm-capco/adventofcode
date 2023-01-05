from math import inf

import input
import re
import operator

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '=': operator.eq
}


class Monkey:

    def __init__(self, name: str, number: int = None, operand1=None, operand2=None, operator=None, human: bool = False):
        self.name = name
        self.number = number
        self.operand1 = operand1
        self.operand2 = operand2
        self.operator = operator
        self.human = human

    def resolve_operands(self, monkeys: dict):
        if (self.number is None and self.name != 'root') or self.operand1 is None or self.operand2 is None:
            return
        op1 = monkeys[self.operand1].number
        op2 = monkeys[self.operand2].number
        if op1 is None and op2 is None:
            return
        # match self.operator:
        #     case: '=':

        if self.operator == '=':
            if op1 is None:
                monkeys[self.operand1].number = op2
            else:
                monkeys[self.operand2].number = op1
        elif self.operator == '*':
            if op1 is None:
                monkeys[self.operand1].number = self.number / op2
            else:
                monkeys[self.operand2].number = self.number / op1
        elif self.operator == '/':
            if op1 is None:
                monkeys[self.operand1].number = self.number * op2
            else:
                monkeys[self.operand2].number = op1 / self.number
        elif self.operator == '+':
            if op1 is None:
                monkeys[self.operand1].number = self.number - op2
            else:
                monkeys[self.operand2].number = self.number - op1
        elif self.operator == '-':
            if op1 is None:
                monkeys[self.operand1].number = self.number + op2
            else:
                monkeys[self.operand2].number = op1 - self.number

    def __str__(self):
        msg = f'{self.name}: {self.number}'
        if self.operator is not None:
            msg += f', {self.operand1} {self.operator} {self.operand2}'
        return msg

    def __repr__(self):
        return self.__str__()


def parse_input(source: list[str]):
    monkeys = dict()
    for line in source:
        result = re.match("([a-z]*): ([0-9]+)", line)
        if result is not None:
            monkeys[result[1]] = Monkey(result[1], int(result[2]))
        else:
            result = re.match("([a-z]+): ([a-z]+) ([+\-*/]) ([a-z]+)", line)
            monkeys[result[1]] = Monkey(result[1], operand1=result[2], operator=result[3], operand2=result[4])

    return monkeys


def part1(monkeys: dict[str: Monkey]):
    return get_monkey_value(monkeys, monkeys['root'])


def get_monkey_value(monkeys: dict[str: Monkey], monkey: Monkey):
    if monkey.number is not None:
        return monkey.number
    if monkey.human:
        return None
    monkey1 = get_monkey_value(monkeys, monkeys[monkey.operand1])
    monkey2 = get_monkey_value(monkeys, monkeys[monkey.operand2])
    if monkey1 is None or monkey2 is None:
        return None
    result = ops[monkey.operator](monkey1, monkey2)
    monkey.number = result
    return result


def part2(monkeys: dict[str: Monkey]):
    monkeys['root'].operator = '='
    # monkeys['root'].number = True
    monkeys['humn'] = Monkey('humn', human=True)

    queue = [monkeys['root']]
    while queue:
        m = queue.pop(0)
        value = get_monkey_value(monkeys, m)

        print(m)
        if m.human and value is not None:
            return value

        monkey1 = monkeys[m.operand1]
        monkey2 = monkeys[m.operand2]

        if monkey1.number is None:
            queue.append(monkey1)
        if monkey2.number is None:
            queue.append(monkey2)
        m.resolve_operands(monkeys)


if __name__ == '__main__':
    # source = input.read_strings(21, year=2022, from_file=True, filename='2022/day21test.txt')
    source = input.read_strings(21, year=2022)
    print(source)
    print(len(source))
    monkeys = parse_input(source)

    # result = part1(monkeys)
    result = part2(monkeys)
    print(result)
