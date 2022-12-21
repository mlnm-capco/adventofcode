from numpy import int_

import input
import numpy as np


def mix2(source: list[int], indices: np.ndarray = None):
    if indices is None:
        indices = np.array(list(range(len(source))))
    result = np.array(source)
    # print(result)
    for idx in range(len(result)):
        # print(f'{idx}: {element}')
        actual_idx = np.where(indices == idx)[0][0]
        element = result[actual_idx]
        new_idx = element + actual_idx
        # if new_idx <= 0:
        #     new_idx -= abs(int(new_idx / len(result))) + 1
        # elif new_idx > len(source):
        #     new_idx += int(new_idx / len(result))
        new_idx = new_idx % (len(result) - 1)

        if actual_idx != new_idx:
            indices = np.delete(indices, actual_idx)
            indices = np.insert(indices, new_idx, idx)
            result = np.delete(result, actual_idx)
            result = np.insert(result, new_idx, element)
    print(result)
    return result, indices


def get_nth_after_zero(source: np.ndarray, n: int):
    zero_i = np.where(source == 0)[0][0]
    target = (zero_i + n) % len(source)
    print(f'Zero at index: {zero_i}, target: {target}')

    return source[target]


def part1(source: list[int]):
    result, _ = mix2(source)
    r1000 = get_nth_after_zero(result, 1000)
    r2000 = get_nth_after_zero(result, 2000)
    r3000 = get_nth_after_zero(result, 3000)
    print(f'{r1000} + {r2000} + {r3000}')
    return result, r1000 + r2000 + r3000


def part2(source: list[int], mixes: int = 10):
    key = 811589153
    source_arr = [e * key for e in source]
    print(f'Pre-mix: {source_arr}')
    indices = None
    result = np.array(source_arr)
    for i in range(mixes):
        print(f"Mix {i}:")
        result, indices = mix2(result, indices)
    print(result)
    r1000 = get_nth_after_zero(result, 1000)
    r2000 = get_nth_after_zero(result, 2000)
    r3000 = get_nth_after_zero(result, 3000)
    print(f'{r1000} + {r2000} + {r3000}')
    return r1000 + r2000 + r3000


if __name__ == '__main__':
    # source = input.read_ints(20, year=2022, from_file=True, filename='2022/day20test.txt')
    source = input.read_ints(20, year=2022)
    print(source)
    print(len(source))

    p1_result, answer = part1(source)
    print(p1_result)
    print(answer)
    # assert str(p1_result) == '[ 1  2 -3  4  0  3 -2]'
    # should be [ 1  2 -3  4  0  3 -2] with result 4 + -3 + 2 = 3

    print(source)
    print(part2(source, 10))

    # 5382459262696
