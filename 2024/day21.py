import input


def part_one(input):
    total = 0
    for code in input:
        sequence = calculate_full_sequence_for_code(code, 3)
        multiplier = code[0:3]
        total += len(sequence) * int(multiplier)
    return total

def test():
    # <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    # v<A<AA>>^AvAA^<A>Av<<A>>^AvA^Av<A>^A<Av<A>>^AAvA^Av<A<A>>^AAAvA^<A>A
    # v<<A>>^A<A>AvA<^AA>A<vAAA>^A
    # <A^A>^^AvvvA
    # 029A
    code = '379A'
    code_moves = translate_code(code)
    directions = translate_directions(code_moves)
    directions2 = translate_directions(directions)
    print(f'{directions2}: {len(directions2)}')
    directions2 = calculate_full_sequence_for_code(code)
    print(f'{directions2}: {len(directions2)}')
    # assert regex.match('<A\^A(>\^\^|\^>\^|\^\^>)AvvvA', code_moves) is not None
    # assert regex.match('v<<A(>>\^|>\^>|\^>>)A<A>AvA(<\^|\^<)AA>A(<v|v<)AAA(>\^|\^>)A', directions) is not None
    # assert regex.match('<vA<AA(>>\^|>\^>|\^>>)AvAA(<\^|\^<)A>A<v<A(>>\^|>\^>|\^>>)AvA\^A(<v|v<)A>\^A(<v<|v<<|<<v)A(>\^|\^>)A>AAvA\^A(<v<|v<<|<<v)A>A(>\^|\^>)AAAvA(<\^|\^<)A>A', directions2) is not None

    # 029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    # 980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
    # 179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
    # 456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
    # 379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A

    # code_980 = calculate_full_sequence_for_code('980A')
    # print(f'{code_980}: {len(code_980)}')
    # code_179 = calculate_full_sequence_for_code('179A')
    # print(f'{code_179}: {len(code_179)}')
    # code_456 = calculate_full_sequence_for_code('456A')
    # print(f'{code_456}: {len(code_456)}')
    # code_379 = calculate_full_sequence_for_code('379A')
    # print(f'{code_379}: {len(code_379)}')

def calculate_full_sequence_for_code(code, levels: int):
    code_moves = translate_code(code, levels)
    directions = translate_directions(code_moves, 1, levels)
    print(f'Directions: {directions}, length: {len(directions)}')
    # directions2 = translate_directions(directions, 2)
    # print(f'Directions 2: {directions2}, length: {len(directions2)}')
    return directions

def translate_code(code: str, levels: int):
    cache = dict()
    current_pos = -1
    chars = [-1 if digit == 'A' else int(digit) for digit in code]
    moves = ''
    for char in chars:
        moves += calculate_keypad_moves(current_pos, char, levels, cache)
        current_pos = char
    print(moves)
    return moves


# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
# level 0: 379A = ^A ^^<<A >>A vvvA
# level 1: ^A ^^<<A >>A vvvA = <A>A <AAv<AA>>^A vAA ^A v<AAA >^A
# level 1: ^A <<^^A >>A vvvA = <A>A v<<AA>^AA>A vAA ^A v<AAA >^A
# level 2: <A>A <AAv<AA>>^AvAA ^A v<AAA >^A = v<<A>>^AvA^A  v<<A>>^AAv<A<A>>^AAvAA^<A>A  v<A>^AA<A>Av<A<A>>^AAAvA^<A>A
# level 2: <A>A v<<AA >^AA >A vAA ^A v<AAA >^A = v<<A>>^AvA^A   v<A<AA>>^AAvA^<A>AAvA^A  v<A>^AA<A>Av<A<A>>^AAAvA^<A>A
def translate_directions(directions: str, level: int, levels: int):
    global directions_cache

    if (directions, level, levels) in directions_cache:
        # print(f'Direction cache hit {len(directions_cache)}: {directions, level}')
        return directions_cache[(directions, level, levels)]

    if level >= levels:
        directions_cache[(directions, level, levels)] = directions
        return directions

    segments = [s + 'A' for s in directions[:-1].split('A')]
    if len(segments) > 1:
        result = ''.join([translate_directions(s, level, levels) for s in segments])
        directions_cache[(directions, level, levels)] = result
        return result

    coords = {'<': (0, 0), 'v': (0, 1), '>': (0,2), '^': (1, 1), 'A': (1, 2)}
    current_row, current_col = coords['A']
    new_moves = ''
    for move in directions:
        target_row, target_col = coords[move]
        ups = target_row - current_row
        lefts = current_col - target_col
        new_moves += calculate_moves(ups, lefts, level, current_row, current_col, levels)
        current_row, current_col = coords[move]

    result = translate_directions(new_moves, level + 1, levels)
    directions_cache[(directions, level, levels)] = result
    return result


# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
def calculate_keypad_moves(current_pos, destination, levels: int, cache: dict):
    if (current_pos, destination) in cache:
        return cache[(current_pos, destination)]
    current_row, current_col = digit_to_position(current_pos)
    target_row, target_col = digit_to_position(destination)
    ups = target_row - current_row
    lefts = current_col - target_col
    new_moves = calculate_moves(ups, lefts, 0, current_row, current_col, levels)

    cache[(current_pos, destination)] = new_moves
    print(f'Keypad {current_pos} to {destination} = {new_moves}')
    return new_moves

def calculate_moves(ups: int, lefts: int, level: int, current_row, current_col, levels: int):
    global moves_cache
    if (ups, lefts, level, levels, current_row, current_col) in moves_cache:
        return moves_cache[(ups, lefts, level, levels, current_row, current_col)]
    # LUDR
    new_moves = ('<' * lefts if lefts > 0 else '>' * -lefts)
    new_moves = new_moves + ('^' * ups if ups > 0 else 'v' * -ups)
    if lefts <= 0  or not is_valid_move(new_moves, level, current_row, current_col):
        new_moves = ('^' * ups if ups > 0 else 'v' * -ups)
        new_moves = new_moves + ('<' * lefts if lefts > 0 else '>' * -lefts)
    new_moves += 'A'
    # if level < levels - 1 and lefts != 0 and ups != 0:
    #     new_moves2 = ''
    #     new_moves2 = new_moves2 + ('<' * lefts if lefts > 0 else '>' * -lefts)
    #     new_moves2 = new_moves2 + ('^' * ups if ups > 0 else 'v' * -ups)
    #     new_moves2 += 'A'
    #     if is_valid_move(new_moves2, level, current_row, current_col):
    #         if not is_valid_move(new_moves, level, current_row, current_col):
    #             new_moves = new_moves2
    #         else:
    #             translated1 = translate_directions(new_moves, level + 1, levels)
    #             translated2 = translate_directions(new_moves2, level + 1, levels)
    #             if len(translated2) < len(translated1):
    #                 new_moves = new_moves2
    moves_cache[(ups, lefts, level, levels, current_row, current_col)] = new_moves
    return new_moves

def is_valid_move(moves, level, current_row, current_col):
    if level == 0:  # numeric keypad
        if current_row == -1 and (current_col == 1 and moves.startswith('<') or current_col == 2 and moves.startswith('<<')):
            return False
        elif current_col == 0 and (current_row == 0 and moves.startswith('v') or current_row == 1 and moves.startswith('vv') or current_row == 2 and moves.startswith('vvv')):
            return False
    else:    # directional keypad
        if current_row == 1 and (current_col == 1 and moves.startswith('<') or current_col == 2 and moves.startswith('<<')):
            return False
        elif current_col == 0 and current_row == 0 and moves.startswith('^'):
            return False
    return True

def test_is_valid_moves():
    assert is_valid_move('<<^^', 0, -1, 2) == False
    assert is_valid_move('<^^', 0, -1, 2)
    assert is_valid_move('<^', 0, -1, 1) == False
    assert is_valid_move('v>>', 0, 0, 0) == False
    assert is_valid_move('vv>', 0, 1, 0) == False
    assert is_valid_move('vvv>>>', 0, 2, 0) == False
    assert is_valid_move('vv>>>', 0, 2, 0)
    assert is_valid_move('v>>>', 0, 1, 0)

    assert is_valid_move('^vvv>>>', 1, 0, 0) == False
    assert is_valid_move('^vvv>>>', 1, 0, 1)
    assert is_valid_move('<v', 1, 1, 1) == False
    assert is_valid_move('<<v', 1, 1, 2) == False
    assert is_valid_move('<v', 1, 1, 2)

def digit_to_position(digit: int):
    if digit == -1:
        return -1, 2
    elif digit == 0:
        return -1, 1
    else:
        return divmod(digit - 1, 3)

def part_two(input):
    total = 0
    for code in input:
        print(f'Processing {code}')
        sequence = calculate_full_sequence_for_code(code, 26)
        multiplier = code[0:3]
        total += len(sequence) * int(multiplier)
    return total

def test2():
    all_moves = set()
    for i in range(-1, 10):
        for j in range(-1, 10):
            if i != j:
                moves = calculate_keypad_moves(i, j)
                all_moves.add(moves)
    print(len(all_moves))

# part one = 211930
# part two = 263492840501566
if __name__ == '__main__':

    test_is_valid_moves()

    directions_cache = dict()
    moves_cache = dict()

    # test2()
    code379 = calculate_full_sequence_for_code('379A', 3)
    print(f'{code379}, {len(code379)}')
    assert len(code379) == 64
    # exit()

    print(directions_cache)
    day = 21
    expected1, expected2 = 126384, -1

    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')

    print(f'Test input: \n{test_input}')

    # Test part 1
    # 68 * 29 + 60 * 980 + 68 * 179 + 64 * 456 + 64 * 379 = 126384
    test_result = part_one(test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    print(f'Directions cache size: {len(directions_cache)}')
    print(directions_cache)

    # Test part 2
    test_result2 = part_two(test_input)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2

    real_input = input.read_strings(day, year=2024, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    real_result = part_one(real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')

