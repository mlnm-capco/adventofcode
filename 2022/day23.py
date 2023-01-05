from copy import copy

import input
from mytypes.grid import Grid, Point


DIRECTIONS = 'NSWE'
VECTORS = {'N': ((-1, -1), (0, -1), (1, -1)), 'S': ((-1, 1), (0, 1), (1, 1)), 'E': ((1, -1), (1, 0), (1, 1)), 'W': ((-1, -1), (-1, 0), (-1, 1))}
ALL_VECTORS = ((-1, -1), (0, -1), (1, -1), (-1, 1), (0, 1), (1, 1), (1, 0), (-1, 0))

def parse_grid(grid: Grid):
    elves = set()
    for j in range(grid.height()):
        for i in range(grid.width()):
            if grid[j][i] == '#':
                elves.add(Point(i, j))
    return elves


def part1(elves: list[Point], turns: int = 10):
    dir = 0
    print_grid(elves)
    for i in range(turns):
        proposed_moves = propose_moves(elves, dir)
        print(f'Turn {i}')
        print(f'Proposed: {proposed_moves}')
        elves, count = do_moves(elves, proposed_moves)
        dir = (dir + 1) % 4
        print(f'Elves: {elves}')
        print_grid(elves)
    return get_answer(elves)


def part2(elves: list[Point]):
    dir, round = 0, 1
    print_grid(elves)
    while True:
        proposed_moves = propose_moves(elves, dir)
        print(f'Round {round}')
        print(f'Proposed: {proposed_moves}')
        elves, count = do_moves(elves, proposed_moves)
        if count == 0:
            return round
        dir = (dir + 1) % 4
        round += 1
        print(f'Elves: {elves}')
        if round % 50 == 0:
            print_grid(elves)


def print_grid(elves: list[Point]):
    min_x = min([p.x for p in elves])
    max_x = max([p.x for p in elves])
    min_y = min([p.y for p in elves])
    max_y = max([p.y for p in elves])
    g = [['.'] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for elf in elves:
        g[elf.y - min_y][elf.x - min_x] = '#'
    print(*[''.join(row) for row in g], sep='\n')


def get_answer(elves: list[Point]):
    grid_area = (max([p.x for p in elves]) - min([p.x for p in elves]) + 1) * (max([p.y for p in elves]) - min([p.y for p in elves]) + 1)
    return grid_area - len(elves)


def propose_moves(elves: set[Point], dir: int = 0):
    proposals = dict()
    for elf in elves:
        has_neighbours = False
        # if no neighbours continue
        for v in ALL_VECTORS:
            checkpoint = Point(elf.x + v[0], elf.y + v[1])
            if checkpoint in elves:
                has_neighbours = True
                break
        if not has_neighbours:
            continue
        for d in range(4):
            direction = DIRECTIONS[(dir + d) % 4]
            vectors = VECTORS[direction]
            found = True
            for v in vectors:
                checkpoint = Point(elf.x + v[0], elf.y + v[1])
                if checkpoint in elves:
                    found = False
                    break
            if found:
                proposed = Point(elf.x + vectors[1][0], elf.y + vectors[1][1])
                if proposed in [p[0] for p in proposals.values()]:
                    duplicate = [k for k, v in proposals.items() if v[0] == proposed][0]
                    proposals[duplicate] = (proposals[duplicate][0], True)
                    proposals[elf] = (proposed, True)
                    break
                else:
                    proposals[elf] = (proposed, False)
                    break
    return proposals


def do_moves(elves: list[Point], proposals: dict[Point: bool]):
    new_elves = set()
    count = 0
    for elf in elves:
        if elf in proposals and not proposals[elf][1]:
            count += 1
            new_pos = proposals[elf][0]
            new_elves.add(new_pos)
        else:
            new_elves.add(elf)
    return new_elves, count


if __name__ == '__main__':
    # source = input.read_strings(23, year=2022, from_file=True, filename='2022/day23test.txt')
    source = input.read_strings(23, year=2022)
    # print(source)
    # print(len(source))
    grid = Grid(source, as_ints=False)
    # print(grid)
    elves = parse_grid(grid)
    # print(elves)
    result = part2(elves)
    print(result)
