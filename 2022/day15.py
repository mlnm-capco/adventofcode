import input
import re

from mytypes.grid import Point


def parse_source(source):
    sensors = {}
    for line in source:
        res = re.match('Sensor at x=([-0-9]*), y=([-0-9]*): closest beacon is at x=([-0-9]*), y=([-0-9]*)', line)
        sensors[Point(int(res[1]), int(res[2]))] = Point(int(res[3]), int(res[4]))
    return sensors


def part1(sensors: dict[Point, Point], line: int = 2000000, min_x: int = -99999999999999, max_x: int = 9999999999999999,
          exc_beacons: bool = True):
    result = set()
    for sensor in sensors:
        beacon = sensors[sensor]
        sensor_range = sensor.manhattan_distance(beacon)
        sensor_dist = abs(line - sensor.y)
        # print(f'Sensor: {sensor}, Range: {sensor_range}, Distance: {sensor_dist}')
        if sensor_range < sensor_dist:
            # print('Out of range')
            continue

        extra = sensor_range - sensor_dist
        result.update(range(max(min_x, sensor.x - extra), min(max_x, sensor.x + extra + 1)))

    for sensor in sensors:
        beacon = sensors[sensor]
        if beacon.y == line and beacon.x in result:
            print(f'Removing beacon at {beacon}')
            result.remove(beacon.x)
    if len(result) < max_x:
        print(f'Row: {line}')
        for i in range(min_x, max_x + 1):
            if i not in result:
                print(f'Column = {i}')
                break
    return len(result)


def search_edges(sensors: dict[Point, Point]):
    count = 0
    for sensor in sensors:
        beacon = sensors[sensor]
        sensor_range = sensor.manhattan_distance(beacon)
        print(f'Searching sensor: {sensor} with range {sensor_range}')
        for d in range(sensor_range + 1):
            count += 1
            if is_in_range(sensor.x + d, sensor.y - (sensor_range + 1) + d, sensors) \
             and is_in_range(sensor.x - d, sensor.y + (sensor_range + 1) - d, sensors) \
             and is_in_range(sensor.x - (sensor_range + 1) + d, sensor.y - d, sensors) \
             and is_in_range(sensor.x + (sensor_range + 1) - d, sensor.y + d, sensors):
                continue
            print(f'Found in {count} iterations')
            return
        print(count)


def is_in_range(x, y, sensors: dict[Point, Point],  _min: int = 0, _max: int = 4000000):
    if x < _min or x > _max or y < _min or y > _max:
        return True
    for sensor in sensors:
        sensor_range = sensor.manhattan_distance(sensors[sensor])
        if Point(x, y).manhattan_distance(sensor) <= sensor_range:
            return True
    print(f'Result: {x}, {y}: {x * 4000000 + y}')
    return False


if __name__ == '__main__':
    # source = input.read_strings(15, year=2022, from_file=True, filename='2022/day15test.txt')
    source = input.read_strings(15, year=2022)
    node_count = 0
    print(source)
    sensors = parse_source(source)
    print(sensors)
    print(len(sensors))
    search_edges(sensors)
