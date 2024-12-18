from enum import Enum

import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray
from numpy._core.strings import isdigit


class Direction(Enum):
    R = 1
    D = 2
    L = 3
    U = 4

    # subtracting gives number of rotations (in either direction) required to get from one to the other
    # X-Y == Y-X for any directions X and Y
    # e.g. L-R == R-L == 2, U-R == R-U == 1
    def __sub__(self, other):
        return min((self.value - other.value) % 4, (other.value - self.value) % 4)

    def rotate(self):
        return Direction(self.value % 4 + 1)

    def to_point(self):
        return {
                Direction.R: Point(1, 0),
                Direction.D: Point(0, 1),
                Direction.L: Point(-1, 0),
                Direction.U: Point(0, -1),
                }[self]

    @staticmethod
    def from_point(point):
        return {
            Point(1, 0): Direction.R,
            Point(0, 1): Direction.D,
            Point(-1, 0): Direction.L,
            Point(0, -1): Direction.U,
        }[point]

    @staticmethod
    def from_char(point):
        return {
            '>': Direction.R,
            'v': Direction.D,
            '<': Direction.L,
            '^': Direction.U,
        }[point]

    def compound(self, operand: int = 0):
        return 2 ** self.value | operand

    def is_included_in(self, compounded):
        if not str(compounded).isdigit():
            return False
        return compounded & 2 ** self.value > 0


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

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return Point(self.x * other, self.y * other)

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def move(self, direction: Direction):
        return self + direction.to_point()

    # rotate 90 degrees clockwise
    # only works for non-diagonal direction vectors
    def rotate(self):
        # TODO must be a simple transformation for this
        _map = {Point(1, 0): Point(0, 1),
               Point(0, 1): Point(-1, 0),
               Point(-1, 0): Point(0, -1),
               Point(0, -1): Point(1, 0)}
        return _map.get(self)

    def to_direction(self):
        _map = {Point(1, 0): 'R',
               Point(0, 1): 'D',
               Point(-1, 0): 'L',
               Point(0, -1): 'U'}
        return _map.get(self)


class Point3D:

    def __init__(self, x: int, y: int, z: int):
        self.x, self.y, self.z = int(x), int(y), int(z)

    def distance(self, other):
        return abs(abs(self.x - other.x)
                   + abs(self.y - other.y)
                   + abs(self.z - other.z))

    def __hash__(self):
        return self.x * 31 + self.y * 37 + self.z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __repr__(self):
        return self.__str__()


class Cuboid:

    def __init__(self, start: Point3D, end: Point3D):
        self._start, self._end = start, end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start: Point3D):
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end: Point3D):
        self._end = end

    def overlap(self, other: 'Cuboid') -> 'Cuboid':
        if (self.start.x <= other.start.x <= self.end.x or self.start.x <= other.end.x <= self.end.x) \
                and (self.start.y <= other.start.y <= self.end.y or self.start.y <= other.end.y <= self.end.y) \
                and (self.start.z <= other.start.z <= self.end.z or self.start.z <= other.end.z <= self.end.z):
            return Cuboid(Point3D(max(self.start.x, other.start.x),
                                  max(self.start.y, other.start.y),
                                  max(self.start.z, other.start.z)),
                          Point3D(min(self.end.x, other.end.x),
                                  min(self.end.y, other.end.y),
                                  min(self.end.z, other.end.z)))
        return None

    def split(self, overlap: 'Cuboid'):
        if overlap is None or overlap == self:
            return [self]
        results = []
        current = self
        while True:
            if current.start.x < overlap.start.x:
                split1, split2 = current.split_x(overlap.start.x - 1)
            elif current.end.x > overlap.end.x:
                split2, split1 = current.split_x(overlap.end.x)
            elif current.start.y < overlap.start.y:
                split1, split2 = current.split_y(overlap.start.y - 1)
            elif current.end.y > overlap.end.y:
                split2, split1 = current.split_y(overlap.end.y)
            elif current.start.z < overlap.start.z:
                split1, split2 = current.split_z(overlap.start.z - 1)
            elif current.end.z > overlap.end.z:
                split2, split1 = current.split_z(overlap.end.z)
            else:
                break
            results.append(split1)
            current = split2
        results.append(overlap)
        return results

    def split_x(self, value: int):
        new_end = Point3D(value, self.end.y, self.end.z)
        new_start = Point3D(value + 1, self.start.y, self.start.z)
        return Cuboid(self.start, new_end), Cuboid(new_start, self.end)

    def split_y(self, value: int):
        new_end = Point3D(self.end.x, value, self.end.z)
        new_start = Point3D(self.start.x, value + 1, self.start.z)
        return Cuboid(self.start, new_end), Cuboid(new_start, self.end)

    def split_z(self, value: int):
        new_end = Point3D(self.end.x, self.end.y, value)
        new_start = Point3D(self.start.x, self.start.y, value + 1)
        return Cuboid(self.start, new_end), Cuboid(new_start, self.end)

    def __len__(self):
        return abs(
            (self._end.x - self._start.x + 1) * (self._end.y - self._start.y + 1) * (self._end.z - self._start.z + 1))

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return (hash(self.start) + 31) * (hash(self.end) + 37)

    def __str__(self):
        return f'{self._start}: {self._end}'

    def __repr__(self):
        return str(self)


def parse_grid(lines: list, as_ints: bool = True):
    if not isdigit(lines[0][0]):
        as_ints = False
    return [[int(char) if as_ints else char for char in line] for line in lines]


def get_neighbours(arr: ndarray, x, y) -> list[Point]:
    neighbours = {(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)}
    return [Point(p[0], p[1]) for p in neighbours if 0 <= p[0] < arr.shape[1] and 0 <= p[1] < arr.shape[0]]


class Grid:

    def __init__(self, lines: list, as_ints:bool = True):
        self.grid = parse_grid(lines, as_ints)

    @staticmethod
    def fill(element, width: int, height: int):
        return Grid([str(element) * width] * height)

    def from_ndarray(self, arr: np.ndarray):
        self.grid = arr.tolist()
        return self

    # returns the given point wrapped back into the grid if necessary
    def normalise(self, operand: Point):
        return Point(operand.x % self.width(), operand.y % self.height())

    def get_neighbours(self, x, y):
        neighbours = {(x + 1, y), (x, y + 1)}
        return [Point(p[0], p[1]) for p in neighbours if 0 <= p[0] < self.width() and 0 <= p[1] < self.height()]

    def get_all_neighbours(self, x, y) -> list[Point]:
        neighbours = {(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)}
        return [Point(p[0], p[1]) for p in neighbours if 0 <= p[0] < self.width() and 0 <= p[1] < self.height()]

    def get_point_neighbours(self, point: Point) -> list[Point]:
        return self.get_all_neighbours(point.x, point.y)

    def get_all_neighbours_inc_diag(self, x, y) -> list[Point]:
        neighbours = {(x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)}
        return [Point(p[0], p[1]) for p in neighbours if 0 <= p[0] < self.width() and 0 <= p[1] < self.height()]

    def populate_points(self, value, points):
        for point in points:
            self[int(point.y)][int(point.x)] = value

    # searches for instances of a word in this grid
    # returns list of tuples (end point, direction)
    def word_search(self, word: str):
        found = []
        for j in range(0, self.height()):
            for i in range(0, self.width()):
                found.extend(self._word_search_from_point(Point(i, j), word))
        return found

    # search for words in any direction in a straight line from a given starting point
    # returns list of tuples (end point, direction)
    def _word_search_from_point(self, start: Point, word: str):
        from collections import deque
        stack = deque([(start, 0, None)])
        found = []
        while len(stack) > 0:
            current, current_index, direction = stack.pop()
            target_char = word[current_index]
            if self[current.y][current.x] == target_char:
                if current_index == len(word) - 1:
                    # print(f'Found match ending at {current} in direction {direction}')
                    found.append((current, direction))
                    continue
                elif direction is None:
                    neighbours = [(p, current_index + 1, p - current)
                                  for p in self.get_all_neighbours_inc_diag(current.x, current.y)]
                    stack.extend(neighbours)
                else:
                    next_cell = current + direction
                    if 0 <= next_cell.x < self.width() and 0 <= next_cell.y < self.height():
                        stack.append((next_cell, current_index + 1, direction))
        return found

    def expand_grid(self):
        np_grid = np.array(self.grid)
        new_grid = np_grid.copy()
        for i in range(1, 5):
            new_grid = np.concatenate([new_grid, (np_grid - 1 + i) % 9 + 1], axis=1)
        long_grid = new_grid.copy()
        for i in range(1, 5):
            new_grid = np.concatenate([new_grid, (long_grid - 1 + i) % 9 + 1], axis=0)
        return self.from_ndarray(new_grid)

    def get(self, location: Point):
        return self.grid[location.y][location.x]

    def __getitem__(self, item):
        return self.grid[item]

    def __setitem__(self, point: Point, value):
        self.grid[point.y][point.x] = value

    def width(self):
        return 0 if self.grid is None else len(self.grid[0])

    def height(self):
        return 0 if self.grid is None else len(self.grid)

    def find(self, item):
        location = next((self.grid[j].index(item), j) for j in range(0, len(self.grid)) if item in self.grid[j])
        return Point(*location)

    def is_inside(self, point: Point) -> bool:
        return 0 <= point.x < self.width() and 0 <= point.y < self.height()

    def plot(self):
        data = self.to_numpy_array()
        data = np.array(list(map(lambda row: list(map(lambda cell: float(hash(str(cell))), row)), self.grid)))
        pixel_plot = plt.figure()
        # pixel_plot.add_axes()

        plt.title("pixel_plot")
        # pixel_plot = plt.imshow(
        #     data, cmap='twilight', interpolation='nearest')
        print(data)
        # ValueError: 'random' is not a valid value for name; supported values are 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'
        pixel_plot = plt.imshow(data, cmap='Pastel1', interpolation='nearest')

        plt.colorbar(pixel_plot)
        plt.savefig('day6_pixel_plot.png')
        plt.show()

    def to_numpy_array(self):
        return np.array(self.grid)

    def __len__(self):
        return len(self.grid)

    def __str__(self):
        return '\n'.join([''.join([e if e != '0' else ' ' for e in map(str, row)]) for row in self.grid])


if __name__ == '__main__':
    # c1 = Cuboid(Point3D(9, 9, 9), Point3D(11, 11, 11))
    # overlap = Cuboid(Point3D(10, 10, 10), Point3D(11, 11, 11))
    # print(c1.split(overlap))
    #
    # c1 = Cuboid(Point3D(11, 11, 11), Point3D(13, 13, 13))
    # overlap = Cuboid(Point3D(11, 11, 11), Point3D(12, 12, 12))
    # print(c1.split(overlap))

    # grid = Grid([['.', '#'], ['o', '.']], as_ints=False)
    # grid.plot()

    print(f'R -> {Direction.R.rotate()}')
    print(f'D -> {Direction.D.rotate()}')
    print(f'L -> {Direction.L.rotate()}')
    print(f'U -> {Direction.U.rotate()}')
    point = Point(5, 4)
    point = point.move(Direction.U)
    print(point)

    compound = 0
    for d in Direction:
        print(f'{compound} + {d}')
        compound = d.compound(compound)
        print(f'L => {Direction.L.is_included_in(compound)}')
        print(f'U => {Direction.U.is_included_in(compound)}')
        print(f'D => {Direction.D.is_included_in(compound)}')
        print(f'R => {Direction.R.is_included_in(compound)}')

    print(Direction.L - Direction.U)
    print(Direction.U - Direction.R)
    print(Direction.R - Direction.D)
    print(Direction.D - Direction.L)
    print(Direction.U - Direction.L)
    print(Direction.L - Direction.D)
    print(Direction.D - Direction.R)
    print(Direction.R - Direction.U)
    print()
    print(Direction.U - Direction.D)
    print(Direction.D - Direction.U)
    print(Direction.L - Direction.R)
    print(Direction.R - Direction.L)