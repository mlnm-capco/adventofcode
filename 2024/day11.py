from collections import deque

import input


def part_one(_stones: list[int]):
    return do_blinks(_stones, 25)

def do_blinks(_stones: list[int], _blinks: int):
    current = _stones
    for i in range(0, _blinks):
        current = blink(current)
        print(f'{i}: {len(current)}')
        # print(f'{current}')
    return len(current)

def blink(_stones: list[int]):
    result = []
    for stone in _stones:
        result.extend(blink_once(stone))
    return result

def blink_once(stone: int):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        middle = int(len(str(stone)) / 2)
        return [int(str(stone)[0: middle]), int(str(stone)[middle:])]
    else:
        return [stone * 2024]

# Part 2

# Doesn't seem to improve performance
def build_cache():
    cache = {}
    for stone in range(0, 10):
        for blinks in range(0, 70):
            get_final_size(stone, blinks, cache)
    return cache

def part_two(_stones):
    _blinks, total = 75, 0
    cache = {}
    for stone in _stones:
        total += get_final_size(stone, _blinks, cache)
    return total

def get_final_size(stone: int, blinks: int, cache: dict):
    if blinks == 0:
        return 1
    elif (stone, blinks) in cache:
        return cache[(stone, blinks)]
    size = sum([get_final_size(s, blinks - 1, cache) for s in blink_once(stone)])
    cache[(stone, blinks)] = size
    return size


# combines blink_once for slight speed-up
def get_final_size_faster(stone: int, blinks: int, cache: dict):
    if blinks == 0:
        return 1
    if (stone, blinks) in cache:
        return cache[(stone, blinks)]
    if len(str(stone)) % 2 == 0:
        middle = int(len(str(stone)) / 2)
        size = get_final_size(int(str(stone)[0: middle]), blinks - 1, cache) + get_final_size(int(str(stone)[middle:]), blinks - 1, cache)
    else:
        size = get_final_size(1 if stone == 0 else stone * 2024, blinks - 1, cache)
    cache[(stone, blinks)] = size
    return size


# part one = 229043
# part two = 272673043446478
if __name__ == '__main__':

    day, test = 11, False
    input = input.read_strings(day, year=2024, from_file=test, filename=f'../input/2024/day{day}test.txt')
    stones = list(map(int, input[0].split()))
    print(f'Input: \n{stones}')

    result = part_one(stones)
    print(f'Part 1: {result}')

    from timeit import default_timer as timer

    start = timer()
    result2 = part_two(stones)
    print(f'Part 2: {result2}')
    print(timer() - start)
    assert result2==272673043446478


