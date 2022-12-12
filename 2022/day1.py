import input


def calculate_totals():
    total = 0
    totals = []
    for val in values:
        if len(val) > 0:
            total += int(val)
        else:
            totals.append(total)
            total = 0
    totals.sort(reverse=True)
    return totals


if __name__ == '__main__':
    values = input.read_strings(1, year=2022)
    totals = calculate_totals()
    print(f'Totals: {totals}')
    print(f'Max: {max(totals)}')
    print(f'Top 3 total: {sum(totals[:3])}')
