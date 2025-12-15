import input
from mytypes.grid import Point, Grid, Line


def part_one(points: list[Point]):
    max_area = 0
    for p in points:
        for q in points:
            if p != q:
                area = (abs(p.x - q.x) + 1) * (abs(p.y - q.y) + 1)
                # print(f'Area {p} to {q} is {area}')
                max_area = max(max_area, area)
    return max_area

def part_two(points: list[Point]):
    lines = parse_as_lines(points)
    max_area = 0
    for p in points:
        for q in points:
            if p != q:
                area = (abs(p.x - q.x) + 1) * (abs(p.y - q.y) + 1)
                # print(f'Area {p} to {q} is {area}')
                if area <= max_area:
                    continue
                intersects = False
                for line in lines:
                    if line.intersects_rectangle(p, q):
                        intersects = True
                        print(f'Points {p} {q}: Lines intersect: {line}')
                        break

                if not intersects:
                    max_area = area
                    print(f'New max area {max_area} between {p} and {q}')
    return max_area

def parse_as_lines(points: list[Point]) -> list[Line]:
    lines = []
    previous_p = None
    for p in points:
        if previous_p is not None:
            lines.append(Line(previous_p, p))
        previous_p = p
    lines.append(Line(previous_p, points[0]))
    return lines

def create_grid(points: list[Point]) -> Grid:
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    grid = Grid.fill('.', max_x + 1, max_y + 1)
    previous_p = None
    for p in points:
        print(p)
        grid[p] = '#'
        if previous_p is not None:
            grid.populate_line('O', Line(previous_p, p), inclusive=False)
        previous_p = p
    grid.populate_line('O', Line(previous_p, points[0]), inclusive=False)
    return grid

def parse_input(input_list):
    return [Point(*line.split(',')) for line in input_list]

# part one = 4771532800
# part two = 1544362560
if __name__ == '__main__':

    day = 9
    expected1, expected2 = 50, 24

    test_input = input.read_strings(day, year=2025, from_file=True, test=True)
    print(f'Test input: \n{test_input}')
    parsed_test_input = parse_input(test_input)
    print(f'Parsed test input: \n{parsed_test_input}')

    # Test part 1
    test_result = part_one(parsed_test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    print(parse_as_lines(parsed_test_input))

    # Test part 2
    test_result2 = part_two(parsed_test_input)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2

    # exit(0)

    real_input = input.read_strings(day, year=2025, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    parsed_real_input = parse_input(real_input)

    print(f'Parsed real input: \n{parsed_real_input}')
    print(parse_as_lines(parsed_real_input))

    real_result = part_one(parsed_real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(parsed_real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
