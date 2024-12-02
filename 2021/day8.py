import input
from mytypes.digit_mapping import Digitmapper


def part1(entries):
    total = 0
    for digits in entries:
        for digit in digits[1]:
            if len(digit) in [2, 3, 4, 7]:
                total += 1
    print(total)


if __name__ == '__main__':
    entries = input.read_digits()
    print(entries)
    total = 0
    for entry in entries:
        mapper = Digitmapper()
        print(f'\nTraining: {entry[0]}, Questions: {entry[1]}')
        mapper.map_digits(entry[0] + entry[1])
        results = mapper.parse_string(entry[1])
        result_int = int(''.join(list(map(str, results))))
        total += result_int
        print(results)
        print(result_int)
    print(total)

