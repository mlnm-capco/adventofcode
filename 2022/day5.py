import input
from collections import deque
import re


def parse_crates(lines: list[str], stack_count: int):
    stacks = [list() for _ in range(stack_count)]
    for line in lines:
        if line.strip().startswith('1'):
            break
        for crate in range(1, len(lines[0]) + 2, 4):
            if crate < len(line) and len(line[crate].strip()) > 0:
                stacks[int((crate - 1) / 4)].insert(0, line[crate])
    print(stacks)
    return stacks


def parse_moves(lines: list[str]):
    moves = []
    pattern = 'move ([0-9]*) from ([0-9]*) to ([0-9]*)'
    for line in lines:
        result = re.search(pattern, line)
        if result is not None:
            moves.append(tuple(int(item) for item in result.groups()))
    return moves


def do_moves(stacks: list[list[str]], moves: list[tuple[int]], individuallly: bool = True):
    for move in moves:
        print('Before:')
        print_crates(stacks)
        print(f'{move}: {stacks[move[1] - 1]}')
        from_stack = stacks[move[1] - 1]
        to_stack = stacks[move[2] - 1]
        to_stack.extend(reversed(from_stack[-move[0]:]) if individuallly else from_stack[-move[0]:])
        stacks[move[1] - 1] = from_stack[0:-move[0]]
        print('After:')
        print_crates(stacks)
    return stacks


def split_input(lines: list[str]):
    for i in range(0, len(lines)):
        if lines[i].strip().startswith('1'):
            stack_count = int(lines[i].rstrip()[-1:])
            return lines[:i], lines[i + 2:], stack_count


def print_crates(crates):
    print(*crates)


def get_tops(stacks: list[list[str]]):
    answer = ''
    for stack in stacks:
        answer = answer + stack.pop()
    return answer


if __name__ == '__main__':
    # values = input.read_strings(5, year=2022, strip=False, from_file=True, filename='2022/day5test.txt')
    values = input.read_strings(5, year=2022, strip=False)
    crates, raw_moves, stack_count = split_input(values)
    print('Crates:')
    print_crates(crates)
    print(f'Stack count: {stack_count}')

    print('Moves:')
    print(*raw_moves)

    stacks = parse_crates(crates, stack_count)
    moves = parse_moves(raw_moves)

    print(*moves, sep='\n')

    moved = do_moves(stacks, moves, individuallly=False)
    answer = get_tops(moved)
    print(answer)