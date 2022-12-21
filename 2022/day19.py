import math
import operator
from copy import copy
from copy import deepcopy

import input
import re


max_geodes = 0
robot_map = dict()


class Blueprint:

    def __init__(self, id, ore_robot_cost, clay_robot_cost, obs_robot_cost_ore, obs_robot_cost_clay,
                 geode_robot_cost_ore, geode_robot_cost_obs):
        self.id = id
        self.costs = [ore_robot_cost, clay_robot_cost, (obs_robot_cost_ore, obs_robot_cost_clay),
                      (geode_robot_cost_ore, geode_robot_cost_obs)]
        self.robots = [1, 0, 0, 0]
        self.resources = [0, 0, 0, 0]
        self.clay_ratio = self.costs[2][1] / self.costs[2][0]       # clay:ore ratio
        self.obsidian_ratio = self.costs[3][1] / self.costs[3][0]   # obsidian:ore ratio
        self.max_ore_cost = max(self.costs[0], self.costs[1], self.costs[2][0], self.costs[3][0])

    def robot_count(self, robot_type: int):
        return self.robots[robot_type]

    def mine(self):
        from operator import add
        self.resources = list(map(add, self.resources, self.robots))

    def robot_options(self):
        can_make_ore_robot = self.resources[0] >= self.costs[0]
        can_make_clay_robot = self.resources[0] >= self.costs[1]
        can_make_obs_robot = self.resources[0] >= self.costs[2][0] and self.resources[1] >= self.costs[2][1]
        can_make_geode_robot = self.resources[0] >= self.costs[3][0] and self.resources[2] >= self.costs[3][1]
        return can_make_ore_robot, can_make_clay_robot, can_make_obs_robot, can_make_geode_robot

    def make_robot(self, type_: int):
        self.robots[type_] += 1
        if type_ <= 1:  # ore/clay
            self.resources[0] -= self.costs[type_]
        else:  # obsidian/geode
            self.resources[0] -= self.costs[type_][0]
            self.resources[type_ - 1] -= self.costs[type_][1]
            if self.resources[type_ - 1] < 0:
                print(f'{"Clay" if type_ == 2 else "Obsidian"} below zero')
                exit(1)
        if self.resources[0] < 0:
            print(f'Ore below zero')
            exit(1)

    def simulate(self, builds: dict[int: int] = None):
        choice = -1
        for i in range(24):
            self.mine()
            if choice >= 0:
                self.make_robot(choice)
            if builds is None:
                choice = self.choose_robot()
            elif i in builds:
                print(i)
                choice = builds[i]
        return self.resources[3]

    def choose_robot(self, elapsed: int = 0, total_minutes: int = 24):
        options = self.robot_options()
        best = len(options) - 1 - options[::-1].index(True) if True in options else -1
        if best == 0:
            ore_needed = max(0, self.costs[1] - self.resources[0])
            current_steps = math.ceil(ore_needed / self.robots[0])
            steps_ore = math.ceil((ore_needed + self.costs[0]) / (self.robots[0]))

            if steps_ore >= current_steps:     # more ore doesn't get to clay any quicker, hold
                best = -1
        elif best == 1 and self.robots[1] > 0:
            ore_needed = max(0, self.costs[2][0] - self.resources[0])
            clay_needed = max(0, self.costs[2][1] - self.resources[1])
            current_steps_ore = math.ceil(ore_needed / self.robots[0])
            current_steps_clay = math.ceil(clay_needed / self.robots[1])
            current_steps = max(current_steps_ore, current_steps_clay)
            steps_clay_ore = math.ceil((ore_needed + self.costs[1]) / (self.robots[0]))
            steps_clay_clay = math.ceil(clay_needed / (self.robots[1] + 1))
            steps_clay = max(steps_clay_ore, steps_clay_clay)

            if steps_clay >= current_steps:     # more clay doesn't get to obsidian any quicker, hold
                best = -1
        elif best == 2 and self.robots[2] > 0:
            ore_needed = max(0, self.costs[3][0] - self.resources[0])
            obsidian_needed = max(0, self.costs[3][1] - self.resources[2])
            current_steps_ore = math.ceil(ore_needed / self.robots[0])
            current_steps_obs = math.ceil(obsidian_needed / self.robots[2])
            current_steps = max(current_steps_ore, current_steps_obs)
            steps_obs_ore = math.ceil((ore_needed + self.costs[2][0]) / (self.robots[0]))
            steps_obs_obs = math.ceil(obsidian_needed / (self.robots[2] + 1))
            steps_obs = max(steps_obs_ore, steps_obs_obs)

            if steps_obs >= current_steps:     # more obsidian doesn't get to geode any quicker, hold
                best = -1
        return best

    def __str__(self):
        return f'Id: {self.id}: Costs: {self.costs}, Resources: {self.resources}, Robots: {self.robots}'


def parse_line(line: str):
    pattern = "Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian."
    res = re.match(pattern, line)
    return Blueprint(*[int(arg) for arg in res.groups()])


def part1(blueprints: list[Blueprint]):
    total = 0
    global max_geodes
    for bp in blueprints:
        max_geodes = 0
        result = dfs(bp)
        print(f'Blueprint {bp.id}: max: {result}, score: {bp.id * result}')
        total += bp.id * result
    return total


def part2(blueprints: list[Blueprint]):
    total = 1
    global max_geodes, robot_map
    for i in range(3):
        if i >= len(blueprints):
            break
        max_geodes = 0
        robot_map = dict()
        result = dfs(blueprints[i], minutes=32)
        total *= result
        print(f'Blueprint {blueprints[i].id}: max: {result}, total: {total}, max geodes: {max_geodes}')
    return total


def dfs(bp: Blueprint, elapsed: int = 0, minutes: int = 32, build: int = -1, skipped=None):
    global max_geodes

    if elapsed == minutes:
        if bp.resources[3] >= max_geodes:
            print(f'New max: {bp}')
        max_geodes = max(max_geodes, bp.resources[3])
        # print(f'Max: {max_geodes}, robots: {bp.robots}, resources: {bp.resources}')
        return bp.resources[3]

    # print(f'Elapsed: {elapsed}, robots: {bp.robots}, resources: {bp.resources}')
    bp = deepcopy(bp)
    bp.mine()
    if build > -1:
        bp.make_robot(build)

    key = f'{elapsed}{bp.resources}'
    if key in robot_map:
        if sum([bp.robots[i] > robot_map[key][i] for i in range(4)]) == 0:
            return 0
    robot_map[key] = bp.robots

    theoretical_max = bp.robots[3] * (minutes - elapsed) + bp.resources[3] + ((minutes - elapsed) / 2) * ((minutes - elapsed) + 1)
    if theoretical_max < max_geodes:
        # print(f'Abandoning, theoretical max = {theoretical_max}')
        return 0

    elapsed += 1

    options = bp.robot_options()

    if sum(options) == 0:
        return dfs(bp, elapsed)

    max_output = 0
    if options[3]:
        max_output = max(max_output, dfs(bp, elapsed, build=3))
    most_obs_needed = (minutes - elapsed) * bp.costs[3][1]
    if options[2] and bp.robots[2] < bp.costs[3][1] and bp.resources[2] < most_obs_needed and (skipped is None or not skipped[2]):
        max_output = max(max_output, dfs(bp, elapsed, build=2))
    most_clay_needed = (minutes - elapsed) * bp.costs[2][1]
    if options[1] and bp.robots[1] < bp.costs[2][1] and bp.resources[1] < most_clay_needed and (skipped is None or not skipped[1]):
        max_output = max(max_output, dfs(bp, elapsed, build=1))
    most_ore_needed = (minutes - elapsed) * max(bp.costs[1], bp.costs[2][0], bp.costs[3][0])
    if options[0] and bp.robots[0] < bp.max_ore_cost and bp.resources[0] < most_ore_needed and (skipped is None or not skipped[0]):
        max_output = max(max_output, dfs(bp, elapsed, build=0))
    if sum(options) < 3:
        max_output = max(max_output, dfs(bp, elapsed, build=-1, skipped=options))

    max_geodes = max(max_geodes, max_output)
    return max_geodes


def run_blueprint(bp: Blueprint, minutes: int = 24):
    queue = [(bp, 0)]
    max_output = 0
    geodes_map = dict()
    while queue:
        current_bp, elapsed = queue.pop(0)
        if len(queue) % 100 == 0:
            print(f'Queue: {len(queue)}, elapsed: {elapsed}, geodes: {current_bp.resources[3]}, max geodes: {max_output}')
        # if elapsed in geodes_map and geodes_map[elapsed] > current_bp.resources[3]:
        #     continue
        current_bp.mine()
        if elapsed == minutes:
            max_output = max(max_output, current_bp.resources[3])
            continue
        options = current_bp.robot_options()
        while sum(options) == 0 and elapsed < minutes - 1:
            current_bp.mine()
            options = current_bp.robot_options()
            elapsed += 1

        if options[3]:
            current_bp.make_robot(3)
            # geode_projection = current_bp.robots[3] * minutes - elapsed
            queue.append((current_bp, elapsed + 1))
            if elapsed in geodes_map:
                geodes_map[elapsed] = max(geodes_map[elapsed], current_bp.resources[3])
            else:
                geodes_map[elapsed] = current_bp.resources[3]
            continue
        elif options[2]:
            if current_bp.robots[2] < current_bp.costs[3][1]:
                current_bp.make_robot(2)
                queue.append((current_bp, elapsed + 1))
                continue
        elif options[1]:
            if current_bp.robots[1] == 0:
                current_bp.make_robot(1)
                queue.append((current_bp, elapsed + 1))
                continue
            if current_bp.robots[1] < current_bp.costs[2][1]:
                bp_copy = deepcopy(current_bp)
                bp_copy.make_robot(1)
                queue.append((bp_copy, elapsed + 1))
        if options[0]:
            max_ore_cost = max(current_bp.costs[0], current_bp.costs[1], current_bp.costs[2][0], current_bp.costs[3][0])
            if current_bp.robots[0] < max_ore_cost:
                bp_copy = deepcopy(current_bp)
                bp_copy.make_robot(0)
                queue.append((bp_copy, elapsed + 1))
        queue.append((current_bp, elapsed + 1))  # the make nothing case
        # for i in [1, 0]:
        #     if options[i]:
        #         bp_copy = deepcopy(current_bp)
        #         bp_copy.make_robot(type_=i)
        #         queue.append((bp_copy, elapsed + 1))
        #         while not options[i + 1] and elapsed < minutes:
        #             current_bp.mine()
        #             options = current_bp.robot_options()
        #             elapsed += 1
        #         if options[i + 1]:
        #             current_bp.make_robot(i + 1)
        #             queue.append((current_bp, elapsed + 1))
    print(f'Blueprint {bp.id} max output: {max_output}')
    return max_output


if __name__ == '__main__':
    # lines = input.read_strings(19, year=2022, from_file=True, filename='2022/day19test.txt')
    lines = input.read_strings(19, year=2022)
    blueprints = []
    for line in lines:
        blueprints.append(parse_line(line))
    print(*blueprints, sep='\n')
    # part1(blueprints)
    # print(blueprints[0].simulate({2: 1, 4: 1, 6: 1, 10: 2, 11: 1, 14: 2, 17: 3, 20: 3}))
    # print(blueprints[0].simulate({2: 1, 4: 1, 6: 1, 8: 1, 10: 2, 14: 2, 17: 3, 20: 3}))

    # print(blueprints[0].simulate())
    # print(blueprints[0])
    # print(blueprints[1].simulate())
    # print(blueprints[1])

    # run_blueprint(blueprints[0])

    print(part2(blueprints))
