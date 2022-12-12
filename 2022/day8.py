import input
from mytypes.grid import Grid


def get_visible(grid: Grid):
    visible_grid = [[0] * grid.width() for i in range(0, grid.height())]

    current = [-1] * grid.width()
    for i in range(0, grid.height()):
        for j in range(0, grid.width()):
            if grid[i][j] > current[j]:
                current[j] = grid[i][j]
                visible_grid[i][j] = 1

    current = [-1] * grid.width()
    for i in range(grid.height() - 1, -1, -1):
        for j in range(0, grid.width()):
            if grid[i][j] > current[j]:
                current[j] = grid[i][j]
                visible_grid[i][j] = 1

    current = [-1] * grid.height()
    for j in range(0, grid.width()):
        for i in range(0, grid.height()):
            if grid[i][j] > current[i]:
                current[i] = grid[i][j]
                visible_grid[i][j] = 1

    current = [-1] * grid.height()
    for j in range(grid.width() - 1, -1, -1):
        for i in range(0, grid.height()):
            if grid[i][j] > current[i]:
                current[i] = grid[i][j]
                visible_grid[i][j] = 1

    print(visible_grid)
    return sum([sum(row) for row in visible_grid])


def scenic_scores(grid: Grid):
    best = 0
    for i in range(1, grid.width() - 1):
        for j in range(1, grid.height() - 1):
            best = max(best, scenic_score(grid, i, j))
    return best


def scenic_score(grid: Grid, row: int, col: int):
    total = 1

    score = 0
    for i in range(row - 1, -1, -1):
        score += 1
        if grid[i][col] >= grid[row][col]:
            break
    total = total * score
    print(f'{score} {total}')

    score = 0
    for i in range(row + 1, grid.width()):
        score += 1
        if grid[i][col] >= grid[row][col]:
            break
    total = total * score
    print(f'{score} {total}')

    score = 0
    for j in range(col - 1, -1, -1):
        score = score + 1
        if grid[row][j] >= grid[row][col]:
            break
    total = total * score
    print(f'{score} {total}')

    score = 0
    for j in range(col + 1, grid.height()):
        score += 1
        if grid[row][j] >= grid[row][col]:
            break
    total = total * score
    print(f'{score} {total}')

    print(f'{row}, {col}: {total}')
    return total


if __name__ == '__main__':
    grid = input.read_grid(8, year=2022, from_file=True, filename='2022/day8.txt')
    # grid = input.read_grid(8, year=2022)
    print(f'{grid}')
    print(get_visible(grid))
    print(scenic_scores(grid))
