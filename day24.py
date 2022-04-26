import input


class Instruction:

    def __init__(self, instruction: tuple[str, str, str]):
        self.operation, self.operand1, self.operand2 = instruction
        try:
            self.operand2 = int(instruction[2])
        except:
            pass

    def __eq__(self, other):
        return self.operation, self.operand1, self.operand2 == other.operation, other.operand1, other.operand2

    def __hash__(self):
        return self.operation * self.operand1 * self.operand2

    def apply(self, vars: list[int], input: int = None):
        op1 = vars[ord(self.operand1) - 119]
        op2 = self.operand2 if isinstance(self.operand2, int) or len(self.operand2) == 0 else vars[
            ord(self.operand2) - 119]
        # print(f'Applying {self}, operands: {op1, op2}, vars: {vars}')
        output = None
        match self.operation:
            case 'inp':
                output = input
            case 'add':
                output = op1 + op2
            case 'mul':
                output = op1 * op2
            case 'div':
                assert op2 != 0
                output = op1 // op2
            case 'eql':
                output = int(op1 == op2)
            case 'mod':
                assert op1 >= 0 and op2 > 0
                output = op1 % op2
        vars[ord(self.operand1) - 119] = output
        return vars

    def __str__(self):
        return f'{self.operation}: {self.operand1} {self.operand2}'

    def __repr__(self):
        return str(self)


class InstructionSet:

    def __init__(self, instructions: list[tuple[str, str, str]]):
        self.instructions = [Instruction(t) for t in instructions]

    def apply(self, vars: list[int], input: int = None):
        for i in self.instructions:
            i.apply(vars, input)
        return vars

    def __str__(self):
        return str(self.instructions)

    def __repr__(self):
        return str(self) + '\n'


class SimplifiedInstructionSet:

    def __init__(self, instructions: list[tuple[str, str, str]]):
        self.v1, self.v2, self.v3 = int(instructions[4][2]), int(instructions[5][2]), int(instructions[15][2])

    # x = ((z % 26) + v2) != input
    # z = z * (25 * x + 1) + (input + v3) * x
    def apply(self, input, z):
        x = int((z % 26 + self.v2) != input)
        z = z // self.v1
        return z * (25 * x + 1) + (input + self.v3) * x

    def reveng(self, input, output):
        zs = set()
        x = output - input - self.v3
        if x % 26 == 0:
            zs.add(x//26 * self.v1)
        if 0 <= input - self.v2 < 26:
            z0 = output * self.v1
            zs.add(input - self.v2 + z0)
        return zs

    def __str__(self):
        return f'{self.v1, self.v2, self.v3}'

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    instruction_sets = input.read_alu()
    commands, full_sets = [], []
    # for instruction_set in instruction_sets:
    #     commands.append(InstructionSet(instruction_set))
    # print(commands)
    # print(commands[13])
    # print(commands[13].apply([1, 2, 3, 4], 5))

    for instruction_set in instruction_sets:
        simplified = SimplifiedInstructionSet(instruction_set)
        full = InstructionSet(instruction_set)
        commands.append(simplified)
        full_sets.append(full)
    print(commands)

    # print(commands[0])
    # outputs = [commands[0].apply(i, 0) for i in range(1, 10)]
    # print(outputs)

    # zs = [0]
    # for i in range(0, len(commands)):
    #     outputs = set()
    #     for z in zs:
    #         outputs = outputs.union({commands[i].apply(i, z) for i in range(1, 10)})
    #         outputs = {o for o in outputs if o < 700}
    #     print(f'{i}: {outputs}')
    #     zs = list(outputs)

    target_outputs = {0}
    results = {}
    for command_i in range(13, -1, -1):
        valid_zs = set()
        for input in range(0, 10):
        # for input in range(9, 0, -1):
            for output in target_outputs:
                for z_in in commands[command_i].reveng(input, output):
                    valid_zs.add(z_in)
                    results[z_in] = (input,) + results.get(output, ())
                    print(f'Results[{z_in}]: {results[z_in]}')

        print(f'{command_i}: ({len(valid_zs)}): {valid_zs}')
        target_outputs = valid_zs
    print(''.join(str(digit) for digit in results[0]))

# 1:  push input + 12
# 2:  push input + 7 unless input = z%26 + 15
# 3:  push input + 1 unless input = z%26 + 12
# 4:  push input + 2 unless input = z%26 + 11
# 5:  pop, push input + 4 unless input = z%26 - 5
# 6:  push input + 15 unless input = z%26 + 14
# 7:  push input + 11 unless input = z%26 + 15
# 8:  pop, push input +  5 unless input = z%26 - 13
# 9:  pop, push input + 3 unless input = z%26 - 16
# 10: pop, push input + 9 unless input = z%26 - 8
# 11: push input + 2 unless input = z%26 + 15
# 12: pop, push input + 3 unless input = z%26 - 8
# 13: pop, push input + 3 unless input = z%26
# 14: pop, push input + 11 unless input = z%26 - 4

# if input - (z % 26) != v2:
# y = 26                else y = 1
# v1 = 1 or 26 => z = z/26 or z          (shift z right if v1 = 26)
# z = z * 26            else z = z       (shift z left if input - (z % 26) != v2)
# z = z + input + v3    else z = z       (add input and v3 to z if input - (z % 26) != v2)

# if input - (z % 26) != v2:
#   if v1 = 26 pop+push, else push input+v3
# if input - (z % 26) == v2
#  if v1 = 26 pop else do nowt
#
##############
# if v1 == 26: pop
# if input - (z % 26) == v2: push input + v3
##############

# inp w     # w = input
# mul x 0   # x' = 0
# add x z   # x' = z
# mod x 26   # x' = z % 26
# div z 1   # z' = z / v1
# add x 14   # x' = (z % 26) + v2

# eql x w   # x' = (z % 26) + v2 == w
# eql x 0   # x' = (z % 26) + v2 != w
# x' = ((z % 26) + v2) != w

# mul y 0   # y = 0
# add y 25  # y = 25
# mul y x   # y = 25 * x
# add y 1  # y = 25 * x + 1   # = 1 or 26

# mul z y  # z' = z/v1 * (25 * x + 1)

# mul y 0   # y = 0
# add y w   # y = w
# add y 12  # y = w + v3
# mul y x   # y = (w + v3) * x
# add z y   # z = z + (w + v3) * x
# z = z/v1 * (25 * x + 1) + (w + v3) * x

# w = input
# x = ((z % 26) + v2) != input
# z = z/v1 * (25 * x + 1) + (input + v3) * x
