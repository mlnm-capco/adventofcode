import input


def process_instructions(instructions: list[str]):
    i = signal = 0
    total = 1
    adding = False
    display = [' '] * 240
    print(display)
    for cycle in range(1, 241):

        if abs((cycle - 1) % 40 - total) <= 1:
            display[cycle - 1] = '#'

        if (cycle - 20) % 40 == 0:
            signal += total * cycle
            print(f'Cycle {cycle}, total: {total}, signal strength: {total * cycle}, total signal: {signal}')

        if instructions[i].startswith("addx"):
            if adding:
                total += int(instructions[i][5:])
                adding = False
                i += 1
            else:
                adding = True
        else:
            i += 1

    print_grid(display)
    return signal


def print_grid(display):
    for i in range(0, 241, 40):
        print(''.join(display[i: i + 40]))


if __name__ == '__main__':
    # instructions = input.read_strings(10, year=2022, from_file=True, filename='2022/day10test.txt')
    instructions = input.read_strings(10, year=2022)
    print(instructions)
    print(process_instructions(instructions))