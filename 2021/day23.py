import math
import sys
from collections import deque


def all_possible_moves(board, last_move: tuple[int, int] = None, depth=2) -> dict[tuple[int, int], dict[tuple[int, int], int]]:
    result = {}
    for i in range(0, 11):
        if last_move == (0, i):
            continue
        moves = possible_moves(board, (0, i), depth)
        if len(moves) > 0:
            result[(0, i)] = moves
    if len(result) > 0:
        return result
    for room in range(1, 5):
        for pos in range(0, depth):
            if last_move == (room, pos):
                continue
            moves = possible_moves(board, (room, pos), depth)
            if len(moves) > 0:
                result[(room, pos)] = moves
    return result


def possible_moves(board, start: tuple[int, int], depth=2) -> dict[tuple[int, int], int]:
    area, position = start
    amphipod = board[start]
    if amphipod == '.':
        return {}
    result = {}
    cost_to_corridor = 0
    own_room = get_own_room(amphipod)
    if area > 0:  # in a room
        for i in range(0, depth - 1):
            if i < position and board[(area, i)] != '.':   # something on top, can't move
                return {}
        if area == own_room:
            needs_moving = False
            for i in range(depth - 1, position, -1):
                if board[(area, i)] != amphipod:
                    needs_moving = True
                    break
            if not needs_moving:    # already home
                return {}

        if position == 1 and board[(area, 0)] != '.':
            return {}
        if area == own_room:
            if position == 1 or position == 0 and board[(area, 1)] == amphipod:
                return {}
        cost_to_corridor = position + 1  # extra moves required to get into corridor
        position = area * 2  # convert room to corridor position
    # in corridor (or in room with access to corridor)
    corridor = [0, 1, 3, 5, 7, 9, 10]
    for pos in range(0, 11):
        cost = cost_to_corridor
        if pos == position:
            continue
        blocked = False
        for i in range(pos, position, -1 if pos > position else 1):
            if board[(0, i)] != '.':
                blocked = True
                break
        if blocked:
            continue
        cost += abs(pos - position)
        if pos in corridor:
            if position not in corridor:  # can't move from corridor to corridor
                result[(0, pos)] = cost
        else:
            # entrance of room pos/2
            room = int(pos / 2)
            if room == own_room:
                for i in range(depth, 0, -1):
                    if board[(room, i - 1)] == '.':
                        cost += i
                        result[(room, i - 1)] = cost
                        break
                    elif board[(room, i - 1)] != amphipod:
                        break
    return result


def move(board, from_pos: tuple[int, int], to_pos: tuple[int, int]):
    new_board = board.copy()
    new_board[to_pos] = new_board[from_pos]
    new_board[from_pos] = '.'
    return new_board


def play_recursive(board, cost: int = 0, last_move=None, complete_boards: dict = {}, dead_boards=[]):
    key = board_key(board)

    if key in complete_boards.keys():
        # print(cost)
        # print(f'Cost: {cost} + cache: {complete_boards[key]} = {complete_boards[key] + cost}')
        return complete_boards[key]

    if finished_part2(key):
        print(f'Finished')
        complete_boards[key] = cost
        return cost

    if key in dead_boards:
        return 999999999

    all_moves = all_possible_moves(board, last_move, 4)
    if len(all_moves) == 0:
        # print('Dead end')
        # print_board(board)
        dead_boards.append(key)
        return 999999999
    min_cost = sys.maxsize
    for start, moves in all_moves.items():
        for destination, move_cost in moves.items():
            move_cost = int(move_cost * math.pow(10, ['A', 'B', 'C', 'D'].index(board[start])))
            # print(f'{board[start]} from: {start} to: {destination}, cost: {move_cost}')
            new_board = move(board, start, destination)
            cost_to_finish = play_recursive(new_board, 0, destination, complete_boards) + move_cost
            complete_boards[key] = cost_to_finish
            min_cost = min(min_cost, cost_to_finish)
    return min_cost


def board_key(board):
    return ''.join([f'{position[0]}{position[1]}{value}' for position, value in board.items() if value != '.'])


def finished(board):
    return board_key(board) == '10A11A20B21B30C31C40D41D'


def finished_part2(key):
    return key == '10A11A12A13A20B21B22B23B30C31C32C33C40D41D42D43D'


def get_own_room(amphipod: str):
    return ' ABCD'.index(amphipod)


def setup():
    board = {(1, 0): 'A', (1, 1): 'D', (2, 0): 'C', (2, 1): 'D', (3, 0): 'B', (3, 1): 'A', (4, 0): 'B', (4, 1): 'C'}
    for i in range(0, 11):
        board[(0, i)] = '.'
    return board


def setup_part2():
     #D#C#B#A#
     #D#B#A#C#
    board = {(1, 0): 'A', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D',
             (2, 0): 'C', (2, 1): 'C', (2, 2): 'B', (2, 3): 'D',
             (3, 0): 'B', (3, 1): 'B', (3, 2): 'A', (3, 3): 'A',
             (4, 0): 'B', (4, 1): 'A', (4, 2): 'C', (4, 3): 'C'}
    for i in range(0, 11):
        board[(0, i)] = '.'
    return board


def test_data():
    board = {(1, 0): 'B', (1, 1): 'A', (2, 0): 'C', (2, 1): 'D', (3, 0): 'B', (3, 1): 'C', (4, 0): 'D', (4, 1): 'A'}
    for i in range(0, 11):
        board[(0, i)] = '.'
    return board


def complete_board():
    board = {(1, 0): 'A', (1, 1): 'A', (2, 0): 'B', (2, 1): 'B', (3, 0): 'C', (3, 1): 'C', (4, 0): 'D', (4, 1): 'D'}
    for i in range(0, 11):
        board[(0, i)] = '.'
    return board


def print_board(board):
    graphic = '#############\n#'
    for i in range(0, 11):
        graphic += board[(0, i)]
    graphic += '#\n'
    graphic += f'###{board[(1, 0)]}#{board[(2, 0)]}#{board[(3, 0)]}#{board[(4, 0)]}###\n'
    graphic += f'  #{board[(1, 1)]}#{board[(2, 1)]}#{board[(3, 1)]}#{board[(4, 1)]}#  \n'
    graphic += f'  #{board[(1, 2)]}#{board[(2, 2)]}#{board[(3, 2)]}#{board[(4, 2)]}#  \n'
    graphic += f'  #{board[(1, 3)]}#{board[(2, 3)]}#{board[(3, 3)]}#{board[(4, 3)]}#  \n'
    graphic += '  #########   '
    print(graphic)


if __name__ == '__main__':
    # #############
    # #...........#
    # ###A#C#B#B###
    #   #D#D#A#C#
    #   #########
    # board = test_data()
    board = setup_part2()
    print_board(board)
    # (0, x) = corridor space x
    # (1-4, x) = room slot
    # print()
    # board = move(board, (2, 0), (0, 7))
    # board = move(board, (3, 0), (0, 0))
    # print_board(board)
    print(board_key(board))

    # complete = complete_board()
    # print_board(complete)
    # print(board_key(complete))
    # print(finished(complete))

    # all_mvs = all_possible_moves(board)
    # print('\n'.join([f'{amph}: {moves}' for amph, moves in all_mvs.items()]))
    # print()
    print(play_recursive(board))

    # test data: 12521
    # print(f'(0, 7): {possible_moves((0, 7))}')
    # print(f'(4, 0): {possible_moves((4, 0))}')
