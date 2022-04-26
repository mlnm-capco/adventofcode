import input


def move_ine_step(cucumbers):
    pass


def move_once(cucumbers: list[list[int]]):
    right_movers = set()
    for y in range(0, len(cucumbers)):
        for x in range(0, len(cucumbers[0])):
            next_x = x + 1 if x < len(cucumbers[0]) - 1 else 0
            if cucumbers[y][x] == 1 and cucumbers[y][next_x] == 0:
                right_movers.add((x, y))
    for cuke in right_movers:
        next_x = cuke[0] + 1 if cuke[0] < len(cucumbers[0]) - 1 else 0
        cucumbers[cuke[1]][next_x] = 1
        cucumbers[cuke[1]][cuke[0]] = 0

    down_movers = set()
    for y in range(0, len(cucumbers)):
        for x in range(0, len(cucumbers[0])):
            next_y = y + 1 if y < len(cucumbers) - 1 else 0
            if cucumbers[y][x] == 2 and cucumbers[next_y][x] == 0:
                down_movers.add((x, y))
    for cuke in down_movers:
        next_y = cuke[1] + 1 if cuke[1] < len(cucumbers) - 1 else 0
        cucumbers[next_y][cuke[0]] = 2
        cucumbers[cuke[1]][cuke[0]] = 0

    return len(right_movers) + len(down_movers)


def print_all(cucumbers: list[list[int]]):
    for y in range(0, len(cucumbers)):
        print(' '.join(['.>v'[c] for c in cucumbers[y]]))


if __name__ == '__main__':
    cucumbers = input.read_cucumbers(from_file=False, filename='day25test1.txt')
    print_all(cucumbers)
    moved = move_once(cucumbers)
    print(moved)
    print_all(cucumbers)
    no_moves = 1
    while moved > 0:
        no_moves += 1
        moved = move_once(cucumbers)
        print(f'After {no_moves} steps, {moved} cukes moved:')
        print_all(cucumbers)

