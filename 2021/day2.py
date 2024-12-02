import input


def calculateposition(values, use_aim = False):
    horizontal = vertical = aim = 0
    for line in values:
        direction, number = line.split(" ")
        number = int(number)
        # print(f'Dir: {direction}, distance: {number}')
        if direction == "forward":
            horizontal += number
            vertical += aim * number
        else:
            delta = number if direction == "down" else -number
            if use_aim:
                aim += delta
            else:
                vertical += delta

    return vertical * horizontal


if __name__ == '__main__':
    values = input.read_strings(2)
    print(calculateposition(values, False))  # Part 1
    print(calculateposition(values, True))   # Part 2

