import numpy as np


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


def parse_grid(lines: list):
    return [[int(char) for char in line] for line in lines]


class Grid:

    def __init__(self, lines: list):
        self.grid = parse_grid(lines)

    def from_ndarray(self, arr: np.ndarray):
        self.grid = arr.tolist()
        return self

    def get_neighbours(self, x, y):
        neighbours = {(x + 1, y), (x, y + 1)}
        return [Point(p[0], p[1]) for p in neighbours if 0 <= p[0] < self.width() and 0 <= p[1] < self.height()]

    def get_all_neighbours(self, x, y):
        neighbours = {(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)}
        return [Point(p[0], p[1]) for p in neighbours if 0 <= p[0] < self.width() and 0 <= p[1] < self.height()]

    def expand_grid(self):
        np_grid = np.array(self.grid)
        new_grid = np_grid.copy()
        for i in range(1, 5):
            new_grid = np.concatenate([new_grid, (np_grid - 1 + i) % 9 + 1], axis=1)
        long_grid = new_grid.copy()
        for i in range(1, 5):
            new_grid = np.concatenate([new_grid, (long_grid - 1 + i) % 9 + 1], axis=0)
        return self.from_ndarray(new_grid)

    def __getitem__(self, item):
        return self.grid[item]

    def width(self):
        return 0 if self.grid is None else len(self.grid[0])

    def height(self):
        return 0 if self.grid is None else len(self.grid)

    def __len__(self):
        return len(self.grid)

    def __str__(self):
        return '\n'.join([', '.join(map(str, row)) for row in self.grid])


if __name__ == '__main__':
    lines = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    grid = Grid(lines)
    print(grid[1][0])
