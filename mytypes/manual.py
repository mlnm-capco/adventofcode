from mytypes.vent import Point


class Fold:

    def __init__(self, axis, coord: int):
        self.axis = axis.lower()
        self.coord = int(coord)

    def __str__(self):
        return f'Fold along {self.axis}={self.coord}'

    def __repr__(self):
        return self.__str__()


class Manual:

    def __init__(self, lines: [str] = None, points: [Point] = None, folds: [Fold] = None):
        self.dots = set()
        self.folds = []
        self.max_x, self.max_y = 0, 0
        for line in lines:
            if ',' in line:
                dot = Point(*line.split(','))
                self.dots.add(dot)
                self.max_x = max(self.max_x, dot.x)
                self.max_y = max(self.max_y, dot.y)
            elif 'fold' in line:
                self.folds.append(Fold(*line[len('fold along '):].split('=')))

    def apply_folds(self, count: int = 999999):
        while len(self.folds) > 0:
            self.apply_fold()

    def apply_fold(self, index: int = 0):
        print(f'Folds: {self.folds}, dots: {self.dots}')

        fold = self.folds[index]
        new_dots = []
        removed_dots = []

        for point in self.dots:
            if getattr(point, fold.axis) <= fold.coord:
                continue
            new_dim = fold.coord * 2 - getattr(point, fold.axis)
            new_dots.append(Point(new_dim, point.y) if fold.axis == 'x' else Point(point.x, new_dim))
            removed_dots.append(point)
        setattr(self, f'max_{fold.axis}', fold.coord - 1)

        self.folds = self.folds[1:]
        self.dots = self.dots.union(new_dots).difference(removed_dots)

    def __len__(self):
        return len(self.dots)

    def __str__(self):
        dotstr, spacestr = '#', '.'
        pic = [[spacestr] * (self.max_x + 1) for _ in range(0, self.max_y + 1)]
        for dot in self.dots:
            pic[dot.y][dot.x] = dotstr
        for fold in self.folds:
            if fold.axis == 'y':
                pic[fold.coord] = ['-'] * (self.max_x + 1)
            elif fold.axis == 'x':
                for row in pic:
                    row[fold.coord] = '|'
        return '\n'.join([''.join(l) for l in pic])
