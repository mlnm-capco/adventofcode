import copy

import input
from mytypes.grid import Grid, Point, Direction


def part_one(_grid: Grid):
    pos = grid.find('^')
    direction = Direction.U
    total = 0
    while _grid.is_inside(pos):
        if grid.get(pos) != 'X':
            total += 1
        # if grid.get(pos) != '^':
        grid[pos] = 'X'
        new_pos = pos.move(direction)
        if grid.is_inside(new_pos) and grid.get(new_pos) == '#':
            direction = direction.rotate()
        new_pos = pos.move(direction)
        pos = new_pos
    print(f'{grid}\n')
    return total


def part_two(_grid: Grid, start_pos: Point):
    count = 0
    for j in range(0, _grid.height()):
        for i in range(0, _grid.width()):
            if _grid[j][i] == 'X':
                if has_loop(start_pos, Point(i, j)):
                    count += 1
    return count


def has_loop(start_pos: Point, obstruction: Point):
    _grid = read_input()
    # print(obstruction)
    _grid[obstruction] = 'O'
    pos = Point(start_pos.x, start_pos.y)
    direction = Direction.U
    while _grid.is_inside(pos):

        if direction.is_included_in(_grid.get(pos)):

            # print(f'\n{_grid}\n')
            print(f'Loop found, obstruction at {obstruction}')
            # _grid.plot()
            return True

        compound = int(_grid.get(pos)) if str(_grid.get(pos)).isdigit() else 0
        _grid[pos] = direction.compound(compound)
        # _grid[pos] = str(_grid.get(pos)).replace('.', '') + direction.name

        new_pos = pos.move(direction)
        while _grid.is_inside(new_pos) and str(_grid.get(new_pos)) in '#O':
            direction = direction.rotate()
            new_pos = pos.move(direction)
        pos = new_pos
    # print(f'\n{_grid}\n')
    return False


def read_input():
    day, test = 6, False
    filename = f'../input/2024/day{day}test.txt' if test else f'../input/2024/day{day}.txt'
    _input = input.read_grid(day, year=2024, as_ints=False, from_file=False, filename=filename)
    # return copy.deepcopy(_input)
    return _input


# part one = 5086
# part two = 1770
if __name__ == '__main__':

    orig_grid: Grid = None
    grid = read_input()
    start_pos = grid.find('^')

    # input.plot()
    print(f'Input: \n{grid}')

    result = part_one(grid)
    print(f'Part 1: {result}\n**** Part 2 ******')
    assert result == 5086

    # grid.plot()

    print(grid)
    result2 = part_two(grid, start_pos)
    print(f'Part 2: {result2}')


