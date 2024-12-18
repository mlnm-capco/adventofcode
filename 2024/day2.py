import input


def is_safe(report: list):
    increasing = report[1] > report[0]
    current = report[0]
    for value in report[1:]:
        diff = value - current
        if increasing != (diff>0) or diff == 0 or abs(diff) > 3:
            return False
        current = value
    return True


def is_safe_part2(report: list):
    for i in range(len(list)):
        if is_safe(report[:i] + report[i+1:]):
            return True
    return False


# part one = 287
# part two = 354
if __name__ == '__main__':

    list = input.read_list_of_ints(2, year=2024)

    print(f'List 1: {list}')

    result = [is_safe(report) for report in list].count(True)
    print(f'Part 1: {result}')

    result2 = [is_safe_part2(report) for report in list].count(True)
    print(f'Part 2: {result2}')


