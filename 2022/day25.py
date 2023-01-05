import input


def decode(source: str):
    multiplier = 1
    answer = 0
    for c in source[::-1]:
        if c == '=':
            answer -= multiplier * 2
        elif c == '-':
            answer -= multiplier
        else:
            answer += multiplier * int(c)
        multiplier *= 5
    return answer


def encode(source: int):
    residual = source
    answer = ''
    divisor = 1
    while residual > 0:
        quantity = (residual % (divisor * 5))
        digit = int(quantity / divisor)
        if digit == 3:
            char = '='
            residual += (divisor * 5) - quantity
        elif digit == 4:
            char = '-'
            residual += (divisor * 5) - quantity
        else:
            char = str(digit)
            residual -= quantity
        answer += char
        divisor *= 5
    return answer[::-1]


if __name__ == '__main__':
    # source = input.read_strings(25, year=2022, from_file=True, filename='2022/day25test.txt')
    source = input.read_strings(25, year=2022)
    print(source)
    total = 0
    for line in source:
        result = decode(line)
        total += result
        print(f'{line} = {result}')
    print(f'Result: {total}, encoded = "{encode(total)}"')
