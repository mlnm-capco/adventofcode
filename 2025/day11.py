from collections import deque

import input


def part_one(nodes):
    queue = deque()
    queue.append('you')
    total = 0
    while len(queue) > 0:
        current = queue.popleft()
        if current == 'out':
            total += 1
        if current not in nodes:
            continue
        for neighbor in nodes[current]:
            queue.append(neighbor)
    return total


def part_two(nodes):
    memento = {}
    def dfs(current, intermediates, visited, path):

        if (current, intermediates) in memento:
            # print(f'  Using memoized result for {current} with {intermediates} intermediates: {memento[(current, intermediates)]}')
            return memento[(current, intermediates)]

        if current == 'out':
            print(f'  Found valid path to out with {intermediates} intermediates: {'->'.join(path + ['out'])}')
            return 1 if intermediates >= 2 else 0

        if current not in nodes:
            return 0

        new_intermediates = intermediates + 1 if current in ('fft', 'dac') else intermediates
        total = 0
        for neighbor in nodes[current]:
            if neighbor not in visited:
                total += dfs(neighbor, new_intermediates, visited.union({current}), path + [current])
        memento[(current, intermediates)] = total
        return total

    return dfs('svr', 0, set(), [])

def parse_input(input_list):
    nodes = {}
    for line in input_list:
        node, outputs = line.split(':')
        nodes[node.strip()] = [o.strip() for o in outputs.split(' ') if len(o.strip()) > 0]
    return nodes


# part one = 566
# part two = 331837854931968
if __name__ == '__main__':

    day = 11
    expected1, expected2 = 5, 2

    test_input = input.read_strings(day, year=2025, from_file=True, test=True)
    print(f'Test input: \n{test_input}')
    parsed_test_input = parse_input(test_input)
    print(f'Parsed test input: \n{parsed_test_input}')

    # Test part 1
    test_result = part_one(parsed_test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2

    test_input = input.read_strings(day, year=2025, from_file=True, filename='day11test2.txt', test=True)
    print(f'Test input 2: \n{test_input}')
    parsed_test_input = parse_input(test_input)
    print(f'Parsed test input 2: \n{parsed_test_input}')

    test_result2 = part_two(parsed_test_input)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2

    # exit(0)

    real_input = input.read_strings(day, year=2025, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    parsed_real_input = parse_input(real_input)
    print(f'Parsed real input: \n{parsed_real_input}')
    real_result = part_one(parsed_real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(parsed_real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
