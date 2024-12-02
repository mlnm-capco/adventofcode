import input


def get_modal_bit(values, index):
    return '1' if [val[index:index + 1] for val in values].count('1') >= len(values) / 2 else '0'


def invert(operand):
    return ''.join({'0': '1', '1': '0'}[c] for c in operand)


def calc_gamma(values):
    return ''.join([get_modal_bit(values, i) for i in range(0, len(values[0]))])


def part1(values):
    gamma = calc_gamma(values)
    delta = invert(gamma)
    print(f'gamma={gamma}={int(gamma, 2)}\ndelta={delta}={int(delta, 2)}')
    return int(gamma, 2) * int(delta, 2)


def part2(values):
    oxygen = co2 = values
    for i in range(0, len(values[0])):
        oxygen = [v for v in oxygen if v[i: i + 1] == get_modal_bit(oxygen, i)]
        co2 = [v for v in co2 if v[i: i + 1] == invert(get_modal_bit(co2, i))] if len(co2) > 1 else co2
        print(f'{i}: oxygen={oxygen}, co2={co2}')
    return int(oxygen[0], 2) * int(co2[0], 2)


if __name__ == '__main__':
    values = input.read_strings(3)
    print(part1(values))
    print(part2(values))
