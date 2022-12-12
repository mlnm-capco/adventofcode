import input


def parse_input(lines: list[str]):
    return [parse_line(line) for line in lines]


def parse_line(line: str):
    return tuple([tuple([int(s) for s in entries.split('-')]) for entries in line.split(',')])


def fully_contained(pair: tuple[tuple[int]]):
    return (pair[0][0] - pair[1][0]) * (pair[0][1] - pair[1][1]) <= 0
    # return pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1] \
    #     or pair[0][0] >= pair[1][0] and pair[0][1] <= pair[1][1]


def partially_contained(pair: tuple[tuple[int]]):
    return max(pair[0][0], pair[1][0]) <= min(pair[0][1], pair[1][1])


if __name__ == '__main__':
    values = input.read_strings(4, year=2022)
    ranges = parse_input(values)
    print(f'{ranges}')
    total = sum([fully_contained(range) for range in ranges])
    # total = sum([partly_contained(range) for range in ranges])
    print(total)
