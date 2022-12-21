from numpy import bool_, False_, True_, int_

import input
import numpy as np


pieces = [np.array([[True_] * 4], dtype=bool),
          np.array([[False_, True_, False_], [True_] * 3, [False_, True_, False_]], dtype=bool),
          np.array([[True_] * 3, [False_, False_, True_], [False_, False_, True_]], dtype=bool),
          np.array([[True_]] * 4, dtype=bool),
          np.array([[True_] * 2] * 2, dtype=bool)]

highest_point = 0
grid = np.empty(shape=(1000, 7), dtype=bool_)
grid.fill(np.False_)
np.set_printoptions(edgeitems=50)


def part1(moves: str, pieces: int = 2022):
    visited = {}
    global grid
    shape = 0
    rolled = move_index = local_top = 0
    threshold = grid.shape[0] - 25
    for i in range(pieces):
        if i % (10091 * 5 * 10) == 0:
            print(f'{i}: {local_top + rolled}')
        local_top, move_index = drop(moves, shape, local_top, move_index)
        shape = (shape + 1) % 5
        if local_top > grid.shape[0] - 8:
            grid = np.roll(grid, shift=-threshold, axis=0)
            grid[local_top - threshold:] = False_
            local_top -= threshold
            rolled += threshold
        if local_top > 10:
            g_hash = grid_hash(local_top)
            hash = f'{shape}-{move_index:05}-{g_hash}'
            current_top = local_top + rolled
            if hash in visited:
                last_visit, last_top = visited[hash]
                # exact same game state, extrapolate from here
                interval = i - last_visit
                top_delta = current_top - last_top
                remaining = pieces - i
                if remaining % interval == 0:
                    print(f"Iteration {i}: Game state identical to iteration {last_visit}: hash: {hash}, interval: {interval}, previous top: {last_top}, delta: {top_delta}")
                    remaining_intervals = int(remaining / interval)
                    print(f'Remaining pieces: {remaining}, remaining intervals: {remaining_intervals}')
                    result = current_top + (top_delta * remaining_intervals) - 1
                    print(f"Remaining intervals * top delta + current top = {remaining_intervals} * {top_delta} + {current_top - 1} = {result}")
                    return result
            else:
                visited[hash] = (i, current_top)
            #
            #
            # Iteration 2530: Exact same gate state as iteration 820: hash: 1-04857-1107966644049263594526, last top: 1245, remaning: 97470, interval: 1710
            # 1935, 350
            # 3645, 2922
            # remaining = 999999997078
            # interval = 2572

            # 5355, 5494
            # 7065, 8066
    print_grid()
    return local_top + rolled


def print_grid():
    print('--------')
    print(np.array2string(np.flip(grid, 0), formatter={'bool': lambda b: '#' if b else ' '}))


def drop(moves: str, shape: int, top=0, move_index=0):
    x, y = 2, top + 3
    piece = pieces[shape]
    while True:
        # shift
        move = '<>'.index(moves[move_index]) * 2 - 1
        if 0 <= x + move <= 7 - piece.shape[1] and not collides(x + move, y, shape):
            x += move
        move_index = (move_index + 1) % len(moves)
        # drop 1
        if y == 0 or collides(x, y - 1, shape):
            top = max(top, y + piece.shape[0])
            # merge into grid
            merge(x, y, shape)
            break
        y -= 1
    return top, move_index


# returns a hash of the top 10 rows of the grid
def grid_hash(local_top: int):
    return int(''.join(grid[local_top - 10:local_top].flatten().astype(np.int_).astype(str)), base=2)


def collides(x, y, shape:int):
    piece = pieces[shape]
    # print(x, y, piece.shape)
    return np.any(np.logical_and(grid[y:y + piece.shape[0], x:x + piece.shape[1]], piece))


def merge(x, y, shape: int):
    piece = pieces[shape]
    section = grid[y:y + piece.shape[0], x:x + piece.shape[1]]
    grid[y:y + piece.shape[0], x:x + piece.shape[1]] = np.logical_or(piece, section)


if __name__ == '__main__':
    # source = input.read_strings(17, year=2022, from_file=True, filename='2022/day17test.txt')[0]
    source = input.read_strings(17, year=2022)[0]
    print(source)
    print(part1(source, 1000000000000))

# 0: 0
# 1000000: 1504508
# 2000000: 3009020
# 3000000: 4513529
# 4000000: 6018021
# 5000000: 7522527
# 6000000: 9027041
# 7000000: 10531589
# 8000000: 12036055
# 9000000: 13540568
# 10000000: 15045082
# 11000000: 16549590
# 12000000: 18054087
# 13000000: 19558601

# expected: 1514285714288
# actual:   1514285714289
# Iteration 2800: Exact same gate state as iteration 1090: hash: 1-06496-39159011937542570782, last top: 1638, remaning: 999999997200, interval: 1710
