import regex
from fontTools.ttLib.tables.ttProgram import instructions

import input


class Computer:

    def __init__(self, a: int, b: int, c: int, instructions: list[int], identity: bool = False):
        self.a, self.b, self.c, self.instructions, self.output, self.pointer, self.identity = int(a), int(b), int(c), instructions, [], 0, identity

    def __repr__(self):
        return f'A: {self.a}, B: {self.b}, C: {self.c}, instructions: {self.instructions}, output: {self.output}'

    def compute(self):
        self.failed = False
        self.pointer = 0
        while self.pointer < len(self.instructions) - 1:
            instr = self.instructions[self.pointer]
            jumped = self.process_instruction(instr, self.instructions[self.pointer + 1])
            # print(f'After instruction: {instr}({self.instructions[self.pointer + 1]}): {self}')
            if not jumped:
                self.pointer += 2
            if self.failed:
                break
        return self

    # def compute_reverse(self):
    #     self.b =

    def process_instruction(self, opcode, operand):
        op_map = {0: self.adv, 1: self.bxl, 2: self.bst, 3: self.jnz, 4:self.bxc, 5: self.out, 6: self.bdv, 7: self.cdv}
        return op_map[opcode](operand)

    def combo(self, operand: int):
        if operand <=3:
            return operand
        return {4: self.a, 5: self.b, 6: self.c}[operand]

    # 0
    def adv(self, operand: int):
        self.a = int(self.a / (2 ** self.combo(operand)))

    # 1
    def bxl(self, operand: int):
        self.b = int(self.b ^ operand)

    # 2
    def bst(self, operand: int):
        self.b = self.combo(operand) % 8

    # 3
    def jnz(self, operand: int):
        if self.a != 0:
            self.pointer = operand
            return True
        return False

    # 4
    def bxc(self, operand: int):
        self.b = self.b ^ self.c

    # 5
    def out(self, operand: int):
        self.output.append(self.combo(operand) % 8)
        if self.identity and self.output != self.instructions[0: len(self.output)]:
            print(f'Output mismatch: {self.output}: {self.instructions}')
            self.failed = True

    # 6
    def bdv(self, operand: int):
        self.b = int(self.a / (2 ** self.combo(operand)))

    # 7
    def cdv(self, operand: int):
        self.c = int(self.a / (2 ** self.combo(operand)))


def parse_input(_input: str):
    reg_a = regex.match('Register A: ([0-9]*)', _input[0]).group(1)
    reg_b = regex.match('Register B: ([0-9]*)', _input[1]).group(1)
    reg_c = regex.match('Register C: ([0-9]*)', _input[2]).group(1)
    prog = regex.match('Program: (.*)', _input[4]).group(1)
    instructions = list(map(int, prog.split(',')))
    return Computer(reg_a, reg_b, reg_c, instructions)

# If register C contains 9, the program 2,6 would set register B to 1.
# If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
# If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
# If register B contains 29, the program 1,7 would set register B to 26.
# If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
def test():
    assert Computer(0, 0, 9, [2, 6]).compute().b == 1
    assert Computer(10, 0, 9, [5,0,5,1,5,4]).compute().output == [0,1,2]
    c3 = Computer(2024, 0, 9, [0, 1, 5, 4, 3, 0]).compute()
    assert c3.output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert c3.a == 0
    assert Computer(0, 29, 9, [1, 7]).compute().b == 26
    assert Computer(0, 2024, 43690, [4,0]).compute().b == 44354

def part_one(input):
    computer = parse_input(input)
    print(f'Parsed computer: {computer}')
    computer.compute()
    return ','.join([str(n) for n in computer.output])

# Register A: 55593699
# Register B: 0
# Register C: 0
#
# Program: 2,4,1,3,7,5,0,3,1,5,4,4,5,5,3,0
#
# 2, 4 = b = a % 8
# 1, 3 = b = b ^ 3
# 7, 5 = c = a / (2 ** b)
# 0, 3 = a = a / 8
# 1, 5 = b = b ^ 5
# 4, 4 = b = b ^ c
# 5, 5 = output b % 8
# 3, 0 = if a != 0 go to 0
#
#
# b = (a % 8) ^ 3
# c = a / (2 ** ((a % 8) ^ 3))
# a = a / 8
# b = ((a%8)^3)^5 ^ c
# b = (a % 8) ^ 3 ^ 5 ^ int(a / (2 ** ((a % 8) ^ 3)))
# b ^ 3 ^ 5 = (a % 8) ^ (a / (2 ** ((a % 8) ^ 3)))
# output b % 8
#
# Reverse:
# output b % 8 = 0, b = 8, b = 8 + output
# (8 + output) ^ 3 ^ 5

def part_two2(input):
    answer = 1
    while True:
        computer = parse_input(input)
        computer.a = answer
        computer.compute()
        if computer.output == computer.instructions:
            # print(f'Answer: {oct(answer)}, computer: {computer}')
            return answer
        if computer.output == computer.instructions[-(len(computer.output)):]:
            # print(f'Answer: {oct(answer)}, computer: {computer}')
            answer = answer * 8 # or answer * 0o10 or answer << 3
        else:
            answer += 1

# part one =
# part two =
if __name__ == '__main__':

    test()

    day = 17
    expected1, expected2 = '4,6,3,5,6,3,5,2,1,0', 117440

    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')
    print(f'Test input: \n{test_input}')

    # Test part 1
    test_result = part_one(test_input)
    print(f'Part 1 test: {test_result}')
    assert test_result == expected1

    # Test part 2
    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test2.txt')
    test_result2 = part_two2(test_input)
    print(f'Part 2 test: {test_result2}')
    if str(expected2) != '-1':
        assert test_result2 == expected2

    # exit()

    real_input = input.read_strings(day, year=2024, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    real_result = part_one(real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two2(real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
    print(f'Octal result: {oct(result2)}')
    assert result2 == 236539226447469



