from collections import deque

import input


def part_one(input):
    total, previous_price = 0, 0
    for seed in input:
        secret, _ = calculate_secret(int(seed), 2000)
        total += secret

    return total


def calculate_secret(secret, iterations: int):
    deltas = deque()
    previous_price = secret % 10
    price_map = dict()
    for i in range(0, iterations):
        secret = calculate(int(secret))
        price = secret % 10
        if len(deltas) >= 4:
            deltas.popleft()
        deltas.append(str(price - previous_price))
        previous_price = price
        # print(f'secret: {secret}, price: {price}, deltas: {deltas}')
        key = ''.join(deltas)
        if key not in price_map:
            price_map[key] = price
    return secret, price_map


def part_two(input):
    total, previous_price = 0, 0
    price_maps = []
    for seed in input:
        secret, price_map = calculate_secret(int(seed), 2000)
        total += secret
        price_maps.append(price_map)
    print(f'Price maps: {len(price_maps)}')

    price, max_price, max_key = 0, 0, ''
    for i in range(-9, 10):
        for j in range(-9, 10):
            for k in range(-9, 10):
                for l in range(-9, 10):
                    key = str(i) + str(j) + str(k) + str(l)
                    price = 0
                    for pm in price_maps:
                        if key in pm:
                            price += pm[key]
                    if price >= max_price:
                        max_price, max_key = price, key
    print(f'Max price: {max_price}, key: {max_key}')
    return max_price, max_key


def calculate(secret: int):
    secret = ((secret * 64) ^ secret) % 16777216
    secret = (int(secret / 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret

# part one =
# part two = 1964 too low, 2001 too high
if __name__ == '__main__':

    secret, price_map = calculate_secret(123, 10)
    print(secret)
    print(price_map)

    day = 22
    expected1, expected2 = 37327623, 23

    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')
    print(f'Test input: \n{test_input}')

    # Test part 1
    test_result = part_one(test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    test_input2 = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test2.txt')

    max_price, key = part_two(test_input2)
    print(f'Part 2 test: Price: {max_price}, key: {key}')
    if expected2 > -1:
        assert max_price == expected2

    real_input = input.read_strings(day, year=2024, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    real_result = part_one(real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')
    assert real_result == 17262627539

    # Real part 2
    start = timer()
    max_price, key = part_two(real_input)
    print(f'Part 2: Max price: {max_price}, key: {key}')
    print(f'Time: {timer() - start}')


