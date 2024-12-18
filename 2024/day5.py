import input


Rules = dict[int: list[int]]

def part_one(rules: Rules, updates: list[str]):
    total = 0
    for update in updates:
        update_pages = list(map(int, update.split(',')))
        if check_update(rules, update_pages):
            total += update_pages[int(len(update_pages)/2)]

    return total

def check_update(rules: Rules, update: list[int]):
    # print(f'Processing {update}')
    for page in update:
        # print(f'  Page: {page}')
        if page not in rules:
            continue
        for rule in rules[page]:
            # print(f'      Rule: {rule}')
            if rule in update and update.index(rule) < update.index(page):
                print(f'Rejecting {update} as {rule} is before {page}')
                return False
    print(f'Update {update} is valid')
    return True


def reorder_update(rules: Rules, update: list[int]):
    # print(f'Processing {update}')
    for page in update:
        # print(f'  Page: {page}')
        if page not in rules:
            continue
        for rule in rules[page]:
            # print(f'      Rule: {rule}')
            if rule in update and update.index(rule) < update.index(page):
                print(f'Reordering: {update}')
                page_index = update.index(page)
                update[update.index(rule)] = page
                update[page_index] = rule
                print(f'Reordered:  {update}')
                return reorder_update(rules, update)
    print(f'Update {update} is valid')
    return True


def part_two(_input):
    total = 0
    for update in updates:
        update_pages = list(map(int, update.split(',')))
        if check_update(rules, update_pages):
            continue
        if reorder_update(rules, update_pages):
            print(f'Adding {update_pages[int(len(update_pages) / 2)]} for update {update}')
            total += update_pages[int(len(update_pages) / 2)]

    return total


def parse_rules(_input: list[str]):
    rules_tuple = [tuple(s.split('|')) for s in _input if '|' in s]
    rules_dict: Rules = {}
    for rule in rules_tuple:
        current = rules_dict.setdefault(int(rule[0]), [])
        current.append(int(rule[1]))
        rules_dict[int(rule[0])] = current
    return rules_dict
    # return {x: y for x, y in rules_tuple}


# part one = 4905
# part two =
if __name__ == '__main__':

    from timeit import default_timer as timer

    start = timer()
    day = 5
    input = input.read_strings(day, year=2024, from_file=False, filename=f'../input/2024/day{day}test.txt')

    print(f'Input: {input}')

    rules = parse_rules(input[:input.index('')])
    print(f'{rules}')
    # assert len(rules) == 6

    updates = input[input.index('') + 1:]
    print(f'Updates: {updates}')
    # assert len(updates) == 6

    result = part_one(rules, updates)
    print(f'Part 1: {result}\n***********\n')
    # assert result == 143
    #
    end = timer()

    part1_time = end - start

    start2 = timer()
    result2 = part_two(input)
    print(f'Part 2: {result2}')
    end2 = timer()

    print(f'Part one: {part1_time}')
    print(f'Part two: {end2 - start2}')


