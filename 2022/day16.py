import math

import input
import re


queue = []
best = 0
distances = dict()


class Valve:

    def __init__(self, name, flow, connectors):
        self.name = name
        self.flow = flow
        self.connectors = connectors
        self.open = False

    def __str__(self):
        return f'Valve: {self.name}, flow rate: {self.flow}, connects to {self.connectors}'

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


def parse_input(source):
    valves = {}
    for line in source:
        result = re.match('Valve ([A-Z]*) has flow rate=([0-9]*); tunnels? leads? to valves? (.*)$', line)
        valve = Valve(result[1], int(result[2]), result[3].split(', '))
        valves[valve.name] = valve
    print(*valves.values(), sep='\n')
    return valves


def distance(v1: str, v2: str, valves: dict[str: Valve]):
    key = ''.join(sorted([v1, v2]))
    if key in distances:
        return distances[key]
    visited, queue = [], []
    minimum = math.inf
    queue.append((v1, 0))
    while queue:
        v, dist = queue.pop(0)
        visited.append(v)
        for c in valves[v].connectors:
            if c == v2:
                minimum = min(minimum, dist + 1)
            elif c not in visited:
                queue.append((c, 1 + dist))
    distances[key] = minimum
    return minimum


# work out all distances between non-zero nodes
# start AA
# for each open non-zero node:
#   add to queue with:
#       pressure += node.flow * (minute - distance)
#       remove node from open nodes
#
def part_1(valves: dict[str: Valve], start: Valve, minutes: int = 30):
    queue.append((start, minutes, 0, [valve for valve in valves if valves[valve].flow > 0]))
    highest_pressure = 0
    count = 0
    while queue:
        current_valve, minutes, pressure, unvisited = queue.pop(0)
        # print(f'Minutes left: {minutes}: Current valve={current_valve} Cumulative pressure={pressure}, unvisited={unvisited}')
        highest_pressure = max(highest_pressure, pressure)
        if len(unvisited) == 0 or minutes < 1:
            count += 1
            print(f'Pressure: {pressure}, new highest: {highest_pressure}, count: {count}')
            continue
        for valve in unvisited:
            remaining = minutes - distance(valve, current_valve, valves) - 1
            if remaining >= 0:
                queue.append((valve, remaining, pressure + (remaining * valves[valve].flow), list(set(unvisited) - {
                    valve})))

    return highest_pressure


def part_2(valves: dict[str: Valve], start: str, minutes: int = 26):
    queue.append((start, start, minutes, minutes, 0, [valve for valve in valves if valves[valve].flow > 0]))
    max_pressure = 0
    count = 0
    while queue:
        current_valve, ele_valve, minutes_, ele_minutes, pressure, unvisited = queue.pop(0)
        max_pressure = max(max_pressure, pressure)
        # print(f'Minutes left: {minutes_}-{ele_minutes}: Current valve={current_valve}-{ele_valve} pressure={pressure}, highest={max_pressure} unvisited={unvisited}')
        if len(unvisited) == 0 or (minutes_ < 1 and ele_minutes < 1):
            count += 1
            print(f'Pressure: {pressure}, new highest: {max_pressure}, count: {count}, queue: {len(queue)}')
            continue
        for target in unvisited:
            dist_ = distance(target, current_valve, valves)
            remaining = minutes_ - dist_ - 1
            if remaining < 0:
                continue
            for ele_target in unvisited:
                if ele_target == target:
                    continue
                ele_dist_ = distance(ele_target, ele_valve, valves)
                ele_remaining = ele_minutes - ele_dist_ - 1
                if ele_remaining < 0:
                    continue
                remaining = max(0, remaining)
                ele_remaining = max(0, ele_remaining)
                queue.append((target if remaining >= 0 else current_valve, ele_target if ele_remaining >= 0 else ele_valve,
                              remaining, ele_remaining,
                              pressure + (remaining * valves[target].flow) + (ele_remaining * valves[ele_target].flow),
                              list(set(unvisited) - {target, ele_target})))

    return max_pressure


if __name__ == '__main__':
    # source = input.read_strings(16, year=2022, from_file=True, filename='2022/day16test.txt')
    source = input.read_strings(16, year=2022)
    print(source)
    valves = parse_input(source)
    # print(part_1(valves, 'AA'))
    print(part_2(valves, 'AA'))
    # print(*distances.items(), sep='\n')