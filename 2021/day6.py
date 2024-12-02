import input


def dp(fishes: list[int], days: int):
    shoal_sizes = [[1] * 9]
    for d in range(1, days + 1):
        shoal_sizes.append([])
        for i in range(0, 9):
            if i == 0:
                shoal_sizes[d].append(shoal_sizes[d - 1][6] + shoal_sizes[d - 1][8])
            else:
                shoal_sizes[d].append(shoal_sizes[d - 1][i - 1])
    return sum([shoal_sizes[days][f] for f in fishes])


if __name__ == '__main__':
    lanternfish = input.read_lanternfish()
    print(len(lanternfish))
    print(dp(lanternfish, 80))
    print(dp(lanternfish, 256))

    # 80 days = 350917
    # 256 days = 1592918715629
    #
    # n[0][*] = 1
    # n[d][0] = n[d-1][6] + n[d-1][8]
    # n[d][1] = n[d-1][0]
    # n[d][8] = n[d-1][7]
    # n[d][i] = i==0 ? n[d-1][6] + n[d-1][8] : n[d-1][i-1]
