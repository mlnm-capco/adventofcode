# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def readfile():
    filepath = "depths.txt"

    cnt = 0
    last = 9999999999
    with open(filepath, 'r') as file:
        while line := file.readline().rstrip():
            if int(line) > last:
                cnt += 1
            last = int(line)
            print(line)
    return cnt


def windows():
    filepath = "depths.txt"
    with open(filepath, 'r') as file:
        values = [int(line.strip()) for line in file.readlines()]
    return [values[i] > values[i - 3] for i in range(3, len(values))].count(True)
    # print("{}:{}:{}".format(lines[0], lines[3], lines[len(lines) - 1]))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(readfile())
    print(windows())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
