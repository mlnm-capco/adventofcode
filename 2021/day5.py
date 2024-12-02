import input
from mytypes.vent import Vent


def filter_straight(vents: [Vent]):
    return [vent for vent in vents if vent.start.x == vent.end.x or vent.start.y == vent.end.y]


def init_grid(size: int):
    return [[0] * size for _ in range(size)]


if __name__ == '__main__':
    grid_size = 1000
    vents = input.read_vents()
    # vents = filter_straight(vents)
    # print(len(vents))
    grid = init_grid(grid_size)
    for vent in vents:
        vent.mark_grid(grid)
    total = 0
    total += sum([sum([1 for cell in row if cell > 1]) for row in grid])
    print(total)
    # Answers 7438, 21406


