import input
from mytypes.grid import Point, Grid


def part_one(_grid):
    total = 0
    antennae = parse_antennae(_grid)
    print(antennae)
    for antenna, locations in antennae.items():
        print(f'{antenna}: {locations}')
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                antinodes = get_all_antinodes(_grid, locations[i], locations[j])
                for antinode in antinodes:
                    if _grid.is_inside(antinode):
                        if _grid[antinode.y][antinode.x] != '#':
                            total += 1
                            _grid[antinode.y][antinode.x] = '#'
    print(_grid)
    return total


def get_antinodes(point1: Point, point2: Point):
    diff = point2 - point1
    antinode1 = point1 - diff
    antinode2 = point2 + diff
    print(f'{point1}:{point2} = diff: {diff}, anotnodes: {antinode1}, {antinode2}')
    return antinode1, antinode2

def get_all_antinodes(_grid: Grid, point1: Point, point2: Point):
    diff = point2 - point1
    antinodes = []
    antinode = point1
    while _grid.is_inside(antinode):
        antinodes.append(antinode)
        antinode += diff
    antinode = point1 - diff
    while _grid.is_inside(antinode):
        antinodes.append(antinode)
        antinode -= diff

    print(f'{point1}:{point2} = diff: {diff}, anotnodes: {antinodes}')
    return antinodes

def parse_antennae(_grid):
    antennae: dict[str, list] = {}
    for j in range(0, _grid.height()):
        for i in range(0, _grid.width()):
            cell = _grid[j][i]
            if cell != '.':
                antennae.setdefault(cell, []).append(Point(i, j))
    return antennae


def part_two(input):
    return NotImplemented


# part one = 254
# part two = 951
if __name__ == '__main__':

    day, test = 8, False
    input_grid = input.read_grid(day, year=2024, from_file=test, as_ints=False, filename=f'../input/2024/day{day}test.txt')

    print(f'Input: \n{input_grid}')

    result = part_one(input_grid)
    print(f'Part 1: \n{result}')

    result2 = part_two(input_grid)
    print(f'Part 2: \n{result2}')


