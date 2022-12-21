import input
from mytypes.grid import Point, Grid

visited = []
queue = []
shortest = 99999999


def find_route(visited: list[Point], grid: Grid, node: Point):
    visited.append(node)
    queue.append((node, 0))
    min_route = grid.height() * grid.width()

    while queue:
        point, count = queue.pop(0)
        # print(f'{count}: {point}: {grid[point.y][point.x]}')

        if grid[point.y][point.x] == '{':
            print(f'Found end at {point.x}, {point.y} in {count} steps')
            min_route = min(min_route, count)

        for neighbour in grid.get_all_neighbours(point.x, point.y):
            if neighbour not in visited and \
                    ord(grid[neighbour.y][neighbour.x]) - ord(grid[point.y][point.x]) <= 1:
                visited.append(neighbour)
                queue.append((neighbour, count + 1))
    return min_route


if __name__ == '__main__':
    # grid = input.read_grid(12, year=2022, from_file=True, filename='2022/day12test.txt', as_ints=False)
    grid = input.read_grid(12, year=2022, as_ints=False)

    start_point = grid.find('S')
    end = grid.find('E')
    print(start_point)

    grid[start_point.y][start_point.x] = 'a'
    grid[end.y][end.x] = '{'
    print(grid)

    # pt 1
    # min_route = find_route(visited, grid, start_point)

    a_starts = [(grid[j].index('a'), j) for j in range(0, len(grid)) if 'a' in grid[j] and grid[j].index('a') > -1]
    print(a_starts)
    print(f'Number of start points: {len(a_starts)}')
    min_route = 99999999999
    for a in a_starts:
        visited = []
        queue = []
        start_point = Point(a[0], a[1])
        route = find_route(visited, grid, start_point)
        min_route = min(min_route, route)
        print(f'Shortest route from {start_point} is {route}')

    print(f'Shortest route: {min_route}')
