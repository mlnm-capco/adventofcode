def calculateposition(use_aim = False):
    filepath = "day2.txt"
    horizontal = 0
    vertical = 0
    aim = 0
    with open(filepath, 'r') as file:
        while line := file.readline().rstrip():
            direction, number = line.split(" ")
            number = int(number)
            print("Dir: {}, distance: {}".format(direction, number))
            if direction == "forward":
                horizontal += number
                vertical += aim * number
            else:
                delta = number if direction == "down" else -number
                if use_aim:
                    aim += delta
                else:
                    vertical += delta

    return vertical * horizontal


if __name__ == '__main__':
    print(calculateposition(True))

