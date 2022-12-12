import math

import input
import re


def parse_monkeys(instructions: list[str]):
    monkeys = []
    for i in range(0, len(instructions), 7):
        monkeys.append(parse_monkey(instructions, i))

    return monkeys


def parse_monkey(instructions: list[str], i: int):
    index = int(re.match('Monkey ([0-9]*):', instructions[i])[1])
    items = re.match('Starting items: (.*)$', instructions[i + 1])[1].replace(' ', '').split(',')
    op_result = re.match('Operation: new = old ([+-/*]) (.*)$', instructions[i + 2])
    operation = op_result[1]
    operand = op_result[2]
    test = int(re.match('Test: divisible by ([0-9]*)$', instructions[i + 3])[1])
    true_action = int(re.match('If true: throw to monkey ([0-9]*)$', instructions[i + 4])[1])
    false_action = int(re.match('If false: throw to monkey ([0-9]*)$', instructions[i + 5])[1])
    return Monkey(index, items, operation, operand, test, true_action, false_action)



class Monkey:

    def __init__(self, index: int, items: list[int], operation: str, operand: str, test: int, y_target: int,
                 n_target: int):
        self.index = index
        self.items = items
        self.operation = operation
        self.operand = operand
        self.test = test
        self.y_target = y_target
        self.n_target = n_target
        self.inspections = 0

    def __str__(self):
        return f'Monkey: {self.index}, items: {self.items}, operation: {self.operation}, operand: {self.operand}, divisible by: {self.test}, true action: {self.y_target}, false action: {self.n_target}, inspections: {self.inspections}'

    def inspections(self):
        return self.inspections


def process(monkeys: list[Monkey], test_product: int = None, divide: bool = True):
    for monkey in monkeys:
        for item in monkey.items:
            monkey.inspections += 1
            operand = item if monkey.operand == 'old' else monkey.operand
            score = eval(f'{item} {monkey.operation} {operand}')
            if divide:
                score = int(score / 3)
            target = monkey.y_target if score % monkey.test == 0 else monkey.n_target
            score = score if test_product is None else score % test_product
            # print(f'Moving item {item}=>{score} from {monkey.index} to {target}')
            monkeys[target].items.append(score)
            # monkey.items.remove(item)
            # print(f'{monkey}')
            # print(f'{monkeys[target]}')
        monkey.items = []
    # print(*monkeys, sep='\n')


if __name__ == '__main__':
    # instructions = input.read_strings(11, year=2022, from_file=True, filename='2022/day11test.txt')
    instructions = input.read_strings(11, year=2022)
    print(*instructions, sep='\n')
    monkeys = parse_monkeys(instructions)
    print(*monkeys, sep='\n')
    test_product = math.prod([m.test for m in monkeys])
    for i in range(0, 10000):
        print(i)
        process(monkeys, test_product, divide=False)
    monkeys.sort(key=Monkey.inspections, reverse=True)
    print(*monkeys, sep='\n')
    print(monkeys[0].inspections * monkeys[1].inspections)

    # ((((x * 19) ^ 2) + 6) ^ 2) + 3
    # 0 => 2, 3
    # 1 => 2, 0
    # 2 => 1, 3
    # 3 => 0, 1
