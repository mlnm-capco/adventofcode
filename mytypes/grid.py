import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray


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

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


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
    return [[int(char) if as_ints else char for char in line] for line in lines]


def get_neighbours(arr: ndarray, x, y) -> list[Point]:
    neighbours = {(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)}
    return [Point(p[0], p[1]) for p in neighbours if 0 <= p[0] < arr.shape[1] and 0 <= p[1] < arr.shape[0]]


class Grid:

    def __init__(self, lines: list, as_ints:bool = True):
        self.grid = parse_grid(lines, as_ints)

    def from_ndarray(self, arr: np.ndarray):
        self.grid = arr.tolist()
        return self

    def get_neighbours(self, x, y):
        neighbours = {(x + 1, y), (x, y + 1)}
        return [Point(p[0], p[1]) for p in neighbours if 0 <= p[0] < self.width() and 0 <= p[1] < self.height()]

    def get_all_neighbours(self, x, y) -> list[Point]:
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

    def find(self, item):
        location = next((self.grid[j].index(item), j) for j in range(0, len(self.grid)) if item in self.grid[j])
        return Point(*location)

    def plot(self):
        data = self.to_numpy_array()
        data = np.array(list(map(lambda row: list(map(lambda cell: float(ord(cell)), row)), self.grid)))
        pixel_plot = plt.figure()
        # pixel_plot.add_axes()

        plt.title("pixel_plot")
        # pixel_plot = plt.imshow(
        #     data, cmap='twilight', interpolation='nearest')
        print(data)
        # ValueError: 'random' is not a valid value for name; supported values are 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'
        pixel_plot = plt.imshow(data, cmap='Pastel1', interpolation='nearest')

        plt.colorbar(pixel_plot)
        plt.savefig('pixel_plot.png')
        plt.show()

    def to_numpy_array(self):
        return np.array(self.grid)

    def __len__(self):
        return len(self.grid)

    def __str__(self):
        return '\n'.join([''.join(map(str, row)) for row in self.grid])


if __name__ == '__main__':
    # c1 = Cuboid(Point3D(9, 9, 9), Point3D(11, 11, 11))
    # overlap = Cuboid(Point3D(10, 10, 10), Point3D(11, 11, 11))
    # print(c1.split(overlap))
    #
    # c1 = Cuboid(Point3D(11, 11, 11), Point3D(13, 13, 13))
    # overlap = Cuboid(Point3D(11, 11, 11), Point3D(12, 12, 12))
    # print(c1.split(overlap))

    grid = Grid([['.', '#'], ['o', '.']], as_ints=False)
    grid.plot()
