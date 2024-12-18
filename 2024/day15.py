import input
from mytypes.grid import Grid, Point, Direction


def do_move(grid: Grid, pos: Point, move):
    direction = Direction.from_char(move)
    new_pos = pos.move(direction)
    if grid.get(new_pos) == '#':
        return False
    if grid.get(new_pos) == '.' or do_move(grid, new_pos, move):
        grid[new_pos] = grid.get(pos)
        grid[pos] = '.'
        return True
    return False

def find_robot(grid: Grid):
    for idx, row in enumerate(grid):
        if '@' in row:
            return Point(row.index('@'), idx)

def calculate_score(grid: Grid):
    result = 0
    for j in range(0, grid.height()):
        for i in range(0, grid.width()):
            if grid[j][i] in 'O[':
                result += 100 * j + i
    return result

def part_one(grid: Grid, moves: str):
    for move in moves:
        robot_pos = find_robot(grid)
        do_move(grid, robot_pos, move)
    print(grid)
    return calculate_score(grid)

# Part 2

def expand_grid(grid: Grid):
    new_rows = []
    for j in range(0, grid.height()):
        current_row = []
        for i in range(0, grid.width()):
            if grid[j][i] in '.#':
                current_row.extend([grid[j][i]] * 2)
            elif grid[j][i] == 'O':
                current_row.extend(['[', ']'])
            elif grid[j][i] == '@':
                current_row.extend(['@', '.'])
        new_rows.append(current_row)
    return Grid(new_rows)


def do_move2(grid: Grid, pos: Point, move):
    direction = Direction.from_char(move)
    new_pos = pos.move(direction)
    vertical = direction == Direction.U or direction == Direction.D
    if can_move2(grid, pos, move):
        target = grid.get(new_pos)
        if target != '.':
            do_move2(grid, new_pos, move)
            if vertical:
                if target == '[':
                    do_move2(grid, new_pos.move(Direction.R), move)
                if target == ']':
                    do_move2(grid, new_pos.move(Direction.L), move)
        grid[new_pos] = grid.get(pos)
        grid[pos] = '.'
        return True
    return False

def can_move2(grid: Grid, pos: Point, move):
    direction = Direction.from_char(move)
    new_pos = pos.move(direction)
    vertical = direction == Direction.U or direction == Direction.D
    can_move = False
    if grid.get(new_pos) == '#':
        return False
    if grid.get(new_pos) == '.' or can_move2(grid, new_pos, move):
        can_move = True
    if vertical and can_move:
        if grid.get(new_pos) == '[':
            return can_move2(grid, new_pos.move(Direction.R), move)
        elif grid.get(new_pos) == ']':
            return can_move2(grid, new_pos.move(Direction.L), move)
    return can_move

def part_two(grid: Grid, moves: str):
    expanded = expand_grid(grid)
    print(f'Expanded:\n{expanded}')
    for move in moves:
        robot_pos = find_robot(expanded)
        do_move2(expanded, robot_pos, move)
    print(f'Final: \n{expanded}')
    return calculate_score(expanded)

def parse_input(lines: list[str]):
    for i in range(0, len(lines)):
        if len(lines[i].strip()) == 0:
            return Grid(lines[0: i], as_ints=False), ''.join(lines[i + 1:])

# part one =
# part two =
if __name__ == '__main__':

    day = 15
    expected1, expected2 = 10092, 9021

    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')

    grid, moves = parse_input(test_input)
    print(f'Test input: \n{test_input}\nParsed:')
    print(f'Grid:\n{grid}')
    print(f'Moves:\n{moves}')
    print(f'Robot position: {find_robot(grid)}')

    # Test part 1
    test_result = part_one(grid, moves)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    grid, moves = parse_input(test_input)
    test_result2 = part_two(grid, moves)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2



    real_input = input.read_strings(day, year=2024, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1

    grid, moves = parse_input(real_input)
    print(f'Real input: \n{test_input}\nParsed:')
    print(f'Grid:\n{grid}')
    print(f'Moves:\n{moves}')
    print(f'Robot position: {find_robot(grid)}')

    start = timer()
    real_result = part_one(grid, moves)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')


    # Real part 2
    grid, moves = parse_input(real_input)
    start = timer()
    result2 = part_two(grid, moves)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')


