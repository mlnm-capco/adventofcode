import urllib3


def get_input(day):
    url: str = "https://adventofcode.com/2021/day/{}/input".format(day)
    response = urllib3.PoolManager().request("get", url)
    text = response.data
    print(text)


def read_input(day: int):
    with open("day{}.txt".format(day), 'r') as file:
        values = [int(line.strip()) for line in file.readlines()]
    return values


def read_strings(day: int):
    with open("day{}.txt".format(day), 'r') as file:
        values = [line.strip() for line in file.readlines()]
    return values


if __name__ == '__main__':
    get_input(3)
