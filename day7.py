import input


def diff(positions, pos):
    total = 0
    for x in positions:
        total += move_cost(pos - x)
    print(f'Pos: {pos}, cost: {total}')
    return total


def move_cost(i: int):
    # return abs(i) # pt 1
    return int((abs(i) + 1) * (abs(i) / 2))


def find_optimum(positions):
    best = 999999999999999
    for i in range(0, max(positions)):
        best = min(best, diff(positions, i))
    return best


if __name__ == '__main__':
    positions = input.read_csv(7)
    print(find_optimum(positions))
    # part 1 = 347011
    # part 2 = 98181112 too low
    print([(i, move_cost(i)) for i in range(-5, 10)])
