import re
from typing import List, Tuple, Union, Any

DAY = '22'

FULL_INPUT_FILE = f'input/day{DAY}.txt'
TEST_INPUT_FILE_1 = f'input/day{DAY}test1.txt'
TEST_INPUT_FILE_2 = f'input/day{DAY}test2.txt'
TEST_INPUT_FILE_3 = f'input/day{DAY}test3.txt'


def load_data(infile_path: str) -> List[List[Union[str, Any]]]:
    data = []
    with open(infile_path, 'r', encoding='ascii') as infile:
        for line in infile:
            split_data = \
                re.match(r'(\w+) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$',
                         line).groups()
            data.append([split_data[0]] + [int(i) for i in split_data[1:]])
    return data


def overlapping_box(box_a: List[int], box_b: List[int]) -> Tuple[int, ...]:
    max_x, max_y, max_z = [max(box_a[i], box_b[i]) for i in (0, 2, 4)]
    min_xp, min_yp, min_zp = [min(box_a[i], box_b[i]) for i in (1, 3, 5)]
    if min_xp - max_x >= 0 and min_yp - max_y >= 0 and min_zp - max_z >= 0:
        return max_x, min_xp, max_y, min_yp, max_z, min_zp


def count_lit_cubes(data):
    lit_count = 0
    counted_zones = []
    for d in reversed(data):
        mode, box = d[0], d[1:]
        x1, x2, y1, y2, z1, z2 = box
        if mode == 'on':
            dead_cubes = []
            for overlap_box in [overlapping_box(zone, box) for zone in counted_zones]:
                if overlap_box:
                    dead_cubes.append(('on', *overlap_box))
            lit_count += (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
            lit_count -= count_lit_cubes(dead_cubes)
        counted_zones.append(box)
    return lit_count


def part_1(infile_path: str) -> int:
    data = []
    for row in load_data(infile_path):
        x1, x2, y1, y2, z1, z2 = row[1:]
        if x1 <= 50 and x2 >= -50 and y1 <= 50 and y2 >= -50 and z1 <= 50 and z2 >= -50:
            data.append(row)
    lit_count = count_lit_cubes(data)
    return lit_count


def part_2(infile_path: str) -> int:
    data = load_data(infile_path)
    lit_count = count_lit_cubes(data)
    return lit_count


if __name__ == '__main__':
    part1_answer = part_1(FULL_INPUT_FILE)
    print(f'Part 1: {part1_answer}')

    part2_answer = part_2(FULL_INPUT_FILE)
    print(f'Part 2: {part2_answer}')