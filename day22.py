import input
from mytypes.grid import Cuboid


class Powergrid:

    def __init__(self, state: bool = False, cuboid: Cuboid = None):
        self.subgrids = []
        self.cuboid = cuboid
        self.state = state

    def add_subgrid(self, state, cuboid):
        for sub in self.subgrids:
            overlap = cuboid.overlap(sub.cuboid)
            if overlap is None:
                continue
            elif overlap == sub.cuboid:  # sub is fully contained by other
                self.subgrids.remove(sub)
                if state:
                    self.add_subgrid(state, cuboid)
                return
            elif overlap == cuboid:  # other is fully contained by sub
                sub.add_subgrid(state, cuboid)
                return
            else:  # partial - split and recurse
                splits = cuboid.split(overlap)
                for c in splits:
                    self.add_subgrid(state, c)
                return
        if state != self.state:
            self.subgrids.append(Powergrid(state, cuboid))

    def size(self):
        size = 0
        if self.cuboid is not None:
            size = len(self.cuboid) * (-1, 1)[self.state]
        return size + sum([g.size() for g in self.subgrids])

    def __str__(self):
        return f'State: {self.state}, size: {self.size()}, grid: {self.cuboid}, Subgrids: {self.subgrids}'

    def __repr__(self):
        return '{' + f'{self.__str__()}' + '}'


def do_operations(operations):
    universe = Powergrid()
    for state, cuboid in operations:
        print(f'Switching {"on" if state else "off"} {cuboid}')
        universe.add_subgrid(state, cuboid)
    return universe


def part1(operations, limit=9999999999):
    lights = set()
    for state, cuboid in operations:
        print(cuboid)
        for x in range(max(-limit, cuboid.start.x), min(limit, cuboid.end.x) + 1):
            for y in range(max(-limit, cuboid.start.y), min(limit, cuboid.end.y) + 1):
                for z in range(max(-limit, cuboid.start.output), min(limit, cuboid.end.output) + 1):
                    if abs(x) <= 50 and abs(y) <= 50 and abs(y) <= 50:
                        if state:
                            lights.add((x, y, z))
                        elif (x, y, z) in lights:
                            lights.remove((x, y, z))
    return len(lights)


if __name__ == '__main__':
    operations = input.read_cuboids(22, False, 'day22test3.txt')
    print(operations)
    universe = do_operations(operations)
    print(universe)
    print(universe.size())
    # print(part1(operations))  # 587785
