import urllib3
import regex as re

from mytypes.manual import Manual
from mytypes.vent import Vent
from mytypes.grid import Point, Cuboid
from mytypes.grid import Grid
from mytypes.grid import Point3D

SESSION_ID = '53616c7465645f5f15f30b143c26686c48bf4ab3aa46ec6f810e146560d7cee82909b260f8866efba45905ac20cb4508743fa9fe1285a794f8be95b23a10bcd7'


def download_input(day, year: int = 2021):
    session_id = SESSION_ID
    url: str = "https://adventofcode.com/{}/day/{}/input".format(year, day)
    response = urllib3.PoolManager().request("get", url, headers={'Cookie': f'session={session_id}'})
    text = response.data
    return str(text, 'utf-8')


def read_ints(day: int, **kwargs):
    return [int(v) for v in read_strings(day, **kwargs)]


def read_strings(day: int, from_file: bool = False, filename: str = None, year: int = 2021, strip: bool = True):
    return read_strings_from_file(day, filename, strip=strip) if from_file else [line.strip() if strip else line for line in
                                                                    download_input(day, year=year).split('\n')][:-1]


def read_strings_from_file(day: int, filename: str = None, strip: bool = True):
    if filename is None:
        filename = f"day{day}.txt"
    with open(f"../input/{filename}", 'r') as file:
        values = [line.strip() if strip else line for line in file.readlines()]
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


def read_grid(day: int = 9, year=2021, from_file: bool = False, filename: str = None, as_ints: bool = True) -> Grid:
    lines = read_strings(day, from_file, filename, year=year)
    return Grid(lines, as_ints=as_ints)


def parse_grid(lines):
    grid = []
    for line in lines:
        row = []
        for char in line:
            row.append(int(char))
        grid.append(row)
    return grid


def read_graph(day: int = 12, from_file: bool = False, filename: str = None) -> dict:
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


def read_scanners(day: int = 19, from_file=False, filename=None):
    from day19 import Scanner, Point3D
    lines = read_strings(day, from_file, filename)
    scanner = None
    scanners = []
    for line in lines:
        if len(line.strip()) == 0:
            continue
        if line.startswith('---'):
            match = re.match('--- scanner (.*) ---', line)
            index = match.group(1)
            if scanner is not None:
                scanners.append(scanner)
            scanner = Scanner(index)
        else:
            scanner.add_beacon(*[int(coord.strip()) for coord in line.split(',')])
    scanners.append(scanner)
    scanners[0].set_location(Point3D(0, 0, 0))
    return scanners


def read_image_data(day: int = 20, from_file=False, filename=None):
    lines = read_strings(day, from_file, filename)
    enhancement = lines[0]
    input_image = []
    for line in lines[2:]:
        input_image.append(line)
    return enhancement, input_image


def read_cuboids(day: int = 22, from_file=False, filename=None):
    lines = read_strings(day, from_file, filename)
    regex = '(on|off) x=(-?[0-9]+)\\.\\.(-?[0-9]+),y=(-?[0-9]+)\\.\\.(-?[0-9]+),z=(-?[0-9]+)\\.\\.(-?[0-9]+)'
    operations = []
    for line in lines:
        match = re.match(regex, line)
        state = match.group(1) == 'on'
        cuboid = Cuboid(Point3D(
                    min(int(match.group(2)), int(match.group(3))),
                    min(int(match.group(4)), int(match.group(5))),
                    min(int(match.group(6)), int(match.group(7)))),
                Point3D(
                    max(int(match.group(2)), int(match.group(3))),
                    max(int(match.group(4)), int(match.group(5))),
                    max(int(match.group(6)), int(match.group(7)))))
        operations.append((state, cuboid))
    return operations


def read_alu(day: int = 24, from_file=False, filename=None):
    lines = read_strings(day, from_file, filename)
    instructions = []
    current = None
    for line in lines:
        if line.startswith('inp'):
            if current is not None:
                instructions.append(current)
            current = []
            line += ' '
        current.append(tuple(line.split(' ')))
    instructions.append(current)
    return instructions


def read_cucumbers(day: int = 25, from_file=False, filename=None):
    grid = []
    for line in read_strings(day, from_file, filename):
        grid.append(['.>v'.index(c) for c in line])
    return grid


if __name__ == '__main__':
    cuboids = read_cuboids()
    print(cuboids)
    alu = read_alu()
    print(alu)
    print(len(alu))
    print(read_cucumbers(from_file=True, filename='day25test1.txt'))

