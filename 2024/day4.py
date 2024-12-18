import input


def part_one(_grid):
    return _grid.word_search('XMAS')


def part_two(_grid):
    _results = _grid.word_search('MAS')
    a_dict = {}
    found = 0
    for endpoint, direction in _results:
        if direction.x == 0 or direction.y == 0:
            continue
        a_pos = endpoint - direction
        if a_dict.setdefault(a_pos, 0) > 0:
            found += 1
        a_dict[a_pos] = 1
    return found


# part one = 2685
# part two = 2048
if __name__ == '__main__':

    input_grid = input.read_grid(4, year=2024, as_ints=False, from_file=False, filename='../input/2024/day4test.txt')

    print(f'Input: \n{input_grid}')

    results = part_one(input_grid)
    print(f'Part 1: {len(results)}')

    result2 = part_two(input_grid)
    print(f'Part 2: {result2}')


