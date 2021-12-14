from input import read_bingo


def check_card(card):
    if [sum(row) for row in card].count(0) > 0:
        return True
    if [sum(i) for i in zip(*card)].count(0) > 0:
        return True
    return False


def play_bingo(numbers, cards, getlast=False):
    done = {}
    for num in numbers:
        for cardi, card in enumerate(cards):
            for rowi, row in enumerate(card):
                for col, square in enumerate(row):
                    # print(f'{num}:{cardi}:{rowi}:{col}:{square}')
                    if square == num:
                        cards[cardi][rowi][col] = 0
                        if check_card(cards[cardi]):
                            done[cardi] = True
                            if not getlast or len(done) == len(cards):
                                # print(f'{num}:{cardi}:{rowi}:{col}:{square}')
                                # print(cards)
                                return calculate_score(cards[cardi], num)


def calculate_score(card, last_num):
    total = sum([sum(row) for row in card])
    return total * last_num


if __name__ == '__main__':
    numbers, cards = read_bingo()
    print(numbers)
    print(play_bingo(numbers, cards))  # 58374
    print(play_bingo(numbers, cards, True))  # 11377
