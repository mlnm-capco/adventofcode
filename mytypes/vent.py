import itertools


class Point:

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f'{self.x},{self.y}'

    def __repr__(self):
        return f'({self.__str__()})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x * 31 + self.y * 31


class Vent:

    def __init__(self, start: Point, end: Point):
        self.start, self.end = start, end

    def mark_grid(self, grid):
        xdir = 1 if self.start.x < self.end.x else -1
        ydir = 1 if self.start.y < self.end.y else -1
        xrng = list(range(self.start.x, self.end.x + xdir, xdir))
        yrange = list(range(self.start.y, self.end.y + ydir, ydir))
        fill_val = xrng[0] if len(xrng) < len(yrange) else yrange[0]
        rng = list(itertools.zip_longest(xrng, yrange, fillvalue=fill_val))

        # print([f'{i},{j}' for i, j in rng])
        for i, j in rng:
            # print(f'marking: {i}:{j}')
            grid[i][j] += 1

    def __str__(self):
        return f'{self.start} -> {self.end}'

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    vent = Vent(Point(1, 5), Point(3, 7))
    vent2 = Vent(Point(3, 5), Point(1, 7))
    vent3 = Vent(Point(3, 5), Point(3, 7))
    print(vent)
    print(vent2)
    grid = [[0] * 10 for _ in range(10)]
    print(grid)
    vent.mark_grid(grid)
    print(grid)
    vent2.mark_grid(grid)
    vent3.mark_grid(grid)
    print(grid)
