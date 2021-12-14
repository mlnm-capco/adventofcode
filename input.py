import urllib3

from mytypes.manual import Manual
from mytypes.vent import Vent
from mytypes.vent import Point


def download_input(day):
    session_id = '53616c7465645f5fb09ebccfd5223b5c338960e88464b49490214eefaec66ac36c9ce6f3ec42ca81db852ab8effb05c5'
    url: str = "https://adventofcode.com/2021/day/{}/input".format(day)
    response = urllib3.PoolManager().request("get", url, headers={'Cookie':f'session={session_id}'})
    text = response.data
    return str(text, 'utf-8')


def read_ints(day: int):
    return [int(v) for v in read_strings(day)]


def read_strings(day: int, from_file: bool = False, filename: str = None):
    return read_strings_from_file(day, filename) if from_file else [line.strip() for line in download_input(day).split('\n')][:-1]


def read_strings_from_file(day: int, filename: str = None):
    if filename is None:
        filename = f"day{day}.txt"
    with open(f"input/{filename}", 'r') as file:
        values = [line.strip() for line in file.readlines()]
    return values


def read_bingo(day: int = 4):
    lines = read_strings(day)
    numbers = [int(s.strip()) for s in lines[0].split(',')]
    cards = []
    current = []
    for line in lines[2:]:
        if len(line.strip()) == 0:
            cards.append(current)
            current = []
        else:
            current.append([int(s.strip()) for s in line.split()])
    return numbers, cards


def read_vents(day: int = 5):
    lines = read_strings(day)
    vents = []
    for line in lines:
        coords = line.split('->')
        start = Point(*coords[0].strip().split(','))
        end = Point(*coords[1].strip().split(','))
        vent = Vent(start, end)
        vents.append(vent)
    return vents


def read_lanternfish(day: int = 6):
    return read_csv(day)


def read_csv(day):
    return list(map(int, read_strings(day)[0].split(',')))


def read_digits(day: int = 8):
    lines = read_strings(day)
    output = []
    for line in lines:
        splits = line.split('|')
        inputs = splits[0].strip().split(' ')
        outputs = splits[1].strip().split(' ')
        output.append((inputs, outputs))
    return output


def read_grid(day: int = 9, from_file: bool = False):
    grid = []
    lines = read_strings(day, from_file)
    return parse_grid(grid, lines)


def parse_grid(grid, lines):
    for line in lines:
        row = []
        for char in line:
            row.append(int(char))
        grid.append(row)
    return grid


def read_graph(day:int = 12, from_file: bool = False, filename: str = None) -> dict:
    lines = read_strings(day, from_file, filename)
    graph = dict()
    for line in lines:
        add_vertex(graph, tuple(line.split('-')))
    return graph


def add_vertex(graph: dict, vertex: tuple):
    if not vertex[0] in graph:
        graph[vertex[0]] = []
    if not vertex[1] in graph:
        graph[vertex[1]] = []
    graph[vertex[0]].append(vertex[1])
    graph[vertex[1]].append(vertex[0])


def read_manual(day: int = 13, from_file: bool = False, filename: str = None):
    lines = read_strings(day, from_file, filename)
    return Manual(lines)


def read_polymer(day: int = 14, from_file: bool = False, filename: str = None):
    lines = read_strings(day, from_file, filename)
    chain = lines[0]
    template = dict()
    for line in lines[2:]:
        key, value = line.split('->')
        template[key.strip()] = value.strip()
    return chain, template


if __name__ == '__main__':
    print(read_polymer(from_file=True, filename='day14test1.txt'))
