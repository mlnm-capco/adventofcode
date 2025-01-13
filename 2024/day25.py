import input


def part_one(locks, keys):
    total = 0
    for lock in locks:
        for key in keys:
            if sum((lock[i] + key[i] <= 5 for i in range(0, 5))) == 5:
                print(f'Lock {lock} key {key}')
                total += 1
    return total


def part_two(input):
    return NotImplemented

def parse_input(input):
    locks = []
    keys = []
    current = [-1, -1, -1, -1, -1]
    lock, new = True, True
    for line in input:
        if new:
            lock = line == '#####'
            new = False
        if len(line.strip()) == 0:
            if lock:
                locks.append(current)
            else:
                keys.append(current)
            new = True
            current = [-1, -1, -1, -1, -1]
            continue
        for i in range(0, len(line)):
            if line[i] == '#':
                current[i] += 1

    if lock:
        locks.append(current)
    else:
        keys.append(current)

    print(f'Locks: {locks}')
    print(f'Keys: {keys}')
    return locks, keys

# part one =
# part two =
if __name__ == '__main__':

    day = 25
    expected1, expected2 = 3, -1

    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')
    print(f'Test input: \n{test_input}')
    locks, keys = parse_input(test_input)

    # Test part 1
    test_result = part_one(locks, keys)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    test_result2 = part_two(test_input)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2

    real_input = input.read_strings(day, year=2024, from_file=False)
    print(f'Real input: \n{real_input}')
    locks, keys = parse_input(real_input)

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    real_result = part_one(locks, keys)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')


