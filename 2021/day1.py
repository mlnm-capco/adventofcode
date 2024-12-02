import input


def count_increase(values, window_size):
    return [values[i] > values[i - window_size] for i in range(window_size, len(values))].count(True)


if __name__ == '__main__':
    values = input.read_ints(1, year=2021)
    print(f'Part 1 = {count_increase(values, 1)}')
    print(f'Part 2 = {count_increase(values, 3)}')
