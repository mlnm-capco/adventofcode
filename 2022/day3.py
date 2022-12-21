import input


def find_common(contents: str):
    splitpoint = int(len(contents)/2)
    compartment1, compartment2 = contents[:splitpoint], contents[splitpoint:]
    print(f'{compartment1}, {compartment2}')
    common = list(set(compartment1) & set(compartment2))[0]
    return common


def get_priority(character: str):
    priority = ord(character.swapcase()) - 64
    priority = priority if priority <= 26 else priority - 6
    return priority


def part_1(values):
    total = 0
    for val in values:
        common = find_common(val)
        priority = get_priority(common)
        total += priority
    print(f'{total}')


def part_2(contents: str):
    total = 0
    for i in range(3, len(contents) + 1, 3):
        a, b, c = contents[i-3: i]
        common = list(set(a) & set(b) & set(c))[0]
        priority = get_priority(common)
        total += priority
        print(f'{a}, {b}, {c}\nCommon: {common}, priority: {priority}')
    print(total)


if __name__ == '__main__':
    values = input.read_strings(3, year=2022)
    print(f'{values}')
    part_1(values)
    part_2(values)
