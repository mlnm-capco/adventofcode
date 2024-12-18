import input


def parse(_input: str):
    parsed = []
    _adjusted = _input + '0'
    for i in range(0, len(_adjusted), 2):
        # print(f'{_adjusted[i]}:{_adjusted[i + 1]}')
        parsed.extend([int(i / 2)] * int(_adjusted[i]))
        parsed.extend([-1] * int(_adjusted[i + 1]))
    return parsed

def parse_as_dict(_input: str):
    _files_dict = {}
    _adjusted = _input + '0'
    i, pos = 0, 0
    for i in range(0, len(_adjusted), 2):
        _files_dict[int(i / 2)] = (pos, int(_adjusted[i]), int(_adjusted[i + 1]))
        pos += int(_adjusted[i]) + int(_adjusted[i + 1])
    return _files_dict

def calculate_total(parsed_list: list):
    total = 0
    for i, item in enumerate(parsed_list):
        # print(f'{i}: {item} = {i * int(item)}')
        if item > -1:
            total += i * int(item)
    return total

def defrag(parsed_list: list):
    for i in range(len(parsed_list) - 1, 0, -1):
        if parsed_list[i] == -1:
            continue
        first_space = parsed_list.index(-1)
        parsed_list[first_space] = parsed_list[i]
        parsed_list[i] = -1
    return parsed_list

# [(id, pos, len)] = [(0, 0, 2), (1, 3)

# id: (pos, len, spaces)
# 0: (0, 2, 3) =>
# 1: (5, 3, 3) =>
# 2: (11, 1, 3) =>
# 3: (15, 3, 1) =>
def defrag_whole_files_dict(_files: dict):
    for j in range(len(_files) - 1, 0, -1):
        file_start, file_size, _ = _files[j]
        insert_after, min_pos = -1, 999999999
        for i in range(0, len(_files)):
            i_pos, i_len, i_spaces = _files[i]
            next_pos = i_pos + i_len
            if next_pos > file_start or i_spaces < file_size or next_pos >= min_pos:
                continue
            min_pos = next_pos
            insert_after = i
        if insert_after > -1:
            insert_pos, insert_len, insert_spaces = _files[insert_after]
            _files[j] = (insert_pos + insert_len, file_size, insert_spaces - file_size)
            _files[insert_after] = (insert_pos, insert_len, 0)
            if j > 0:
                _files[j - 1] = (_files[j - 1][0], _files[j - 1][1], _files[j - 1][2] + file_size)
    return _files

# 0, 0, 0, 0, 0, 1, 1, 1, 1, 1
def calculate_total_dict(_files: dict):
    total = 0
    for key, item in _files.items():
        total += int(((item[0] + item[0] + item[1] - 1) / 2) * item[1] * key)
    return total

def defrag_whole_files(parsed_list: list):
    i = len(parsed_list) - 1
    while i > 0:
        while file_id := parsed_list[i] == -1:
            i -= 1
        file_start = parsed_list.index(file_id)
        file_length = i - file_start + 1
        first_space = find_space(parsed_list, file_length)
        if 0 <= first_space < file_start:
            parsed_list[first_space: first_space + file_length] = [parsed_list[i]] * file_length
            parsed_list[file_start: file_start + file_length] = [-1] * file_length
        i -= file_length
    return parsed_list

def find_space(parsed_list: list, size: int):
    start_i = 0
    while start_i < len(parsed_list):
        first_space = parsed_list.index(-1, start_i)
        if sum(parsed_list[first_space: first_space + size]) == -1 * size:
            # print(f'Found space at {first_space}')
            return first_space
        else:
            while start_i < len(parsed_list) and parsed_list[start_i] == -1:
                start_i += 1
    return -1

def part_one(parsed_list: list):
    result = defrag(parsed_list)
    return calculate_total(result)

def part_two(parsed_list: list):
    result = defrag_whole_files(parsed_list)
    return calculate_total(result)


# part one = 6338746008070
# part two = 6377400869326
if __name__ == '__main__':

    day, test = 9, False
    input = input.read_strings(day, year=2024, from_file=test, filename=f'../input/2024/day{day}test.txt')[0]

    print(f'Input: {input}')
    parsed = parse(input)
    print(f'Parsed: {parsed}')

    result = part_one(parsed)
    print(f'Part 1: {result}')

    files_dict = parse_as_dict(input)
    print(f'Parsed as dict: {files_dict}')
    defragged = defrag_whole_files_dict(files_dict)
    print(f'Defragged: {defragged}')
    total = calculate_total_dict(defragged)
    print(total)
    # result2 = part_two(files_dict)
    # print(f'Part 2: {result2}')


