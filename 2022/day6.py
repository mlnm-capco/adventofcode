import input


def find_marker(signal: str, length: int = 4):
    return next((i for i in range(length, len(signal) + 1) if len(set(signal[i - length: i])) == length), None)


def test():
    lines = input.read_strings(6, year=2022, from_file=True, filename='2022/day6test.txt')
    assert find_marker(lines[0]) == 5
    assert find_marker(lines[1]) == 6
    assert find_marker(lines[2]) == 10
    assert find_marker(lines[3]) == 11
    assert find_marker(lines[4]) == 11


if __name__ == '__main__':
    signal = input.read_strings(6, year=2022)[0]
    print(signal)
    test()
    print(find_marker(signal, 4))
    print(find_marker(signal, 14))
