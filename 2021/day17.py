import input
from mytypes.grid import Point
import matplotlib.pyplot as plt


def solution(target_bl, target_tr):
    max_y = opt_vx = opt_vy = count = 0

    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()

    for v_y in range(min(0, target_bl.y), int(target_bl.x / 2) - target_tr.y):
        for v_x in range(1, target_tr.x + 1):
            max_height = int(v_y * ((v_y + 1) / 2))
            if _try(target_bl, target_tr, v_x, v_y, ax):
                count += 1
                print(f'Velocity: {v_x, v_y}, max_height: {max_height}')
                max_y = max(max_y, max_height)

    plt.show()
    return count, max_y


def _try(target_bl, target_tr, velocity_x, velocity_y, ax):
    current_x = current_y = 0
    points = []

    while current_y >= target_bl.y and current_x <= target_tr.x:
        if in_target(target_bl, target_tr, current_x, current_y):
            plot(points, ax)
            return True
        current_y += velocity_y
        current_x += velocity_x
        velocity_y -= 1
        velocity_x -= 1
        velocity_x = max(0, velocity_x)
        points.append(Point(current_x, current_y))
    return False


def in_target(target_bl, target_tr, x, y):
    return target_bl.x <= x <= target_tr.x and target_bl.y <= y <= target_tr.y


def get_y_for_x(x: int, y_velocity: int):
    return (x - 1) * (x / 2) + (y_velocity * x)


def plot(points, ax, target_bl = None, target_tr = None):
    import numpy as np

    # make data
    x = [p.x for p in points]
    y = [p.y for p in points]

    ax.plot(x, y, linewidth=2.0)

    ax.set(xlim=(0, max(x) * 1.1), xticks=np.arange(1, max(x) * 1.1),
           ylim=(0, max(y) * 1.1), yticks=np.arange(1, max(y) * 1.1))



def do_maths_stuff(target_bl, target_tr, velocity_x, velocity_y):
    # ls = horiz steps to left edge of target
    # ls =
    # rs = horiz steps to right edge of target
    # rs =

    # vy(s) = vertical velocity after s steps
    # vy = initial_vy - s
    #  y = sum(vy(0) to vy(s))
    #  y = vy(s) * (vy(s) / 2)
    # vy1= vy - 5
    # vy1= s - 1
    #  y = sum(vy1(0) to vy1(s)) + (5 * s)
    #  y = vy1(s) * (s / 2) + (5 * s)
    #  y = (s - 1) * (s / 2) + (initial_vy * s)
    # ty = y value at tx
    # ty = (tx - 1) * (tx / 2) + (initial_vy * tx)

    # vy = 0, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6, -7
    # vy1= 0, 0,-1,-2,-3,-4,-5,-6,-7,-8,-9...
    # y  = 0, 5, 9,12,14,15,15, 14, 12,  9,  5,  0, -6, -13
    ls = target_bl.x / velocity_x
    rs = target_tr.x / velocity_x
    y = get_y_for_x(tx, velocity_y)
    pass



if __name__ == '__main__':
    input.read_strings(17, True, 'day18test1.txt')
    # target area: x=111..161, y=-154..-101
    # (4531, 11781)
    print(solution(Point(111, -154), Point(161, -101)))
    # plot([Point(2, 4), Point(3, 7), Point(8, 10)])
    # 2850 too low
    # x=20..30, y=-10..-5 = 45 with velocity 6,9
    # print(solution(Point(20, -10), Point(30, -5)))


