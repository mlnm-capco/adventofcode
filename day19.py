import day19
import input
import math
from mytypes.grid import Point3D


class Scanner:

    def __init__(self, index: int):
        self.index = index
        self.beacons = set()
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.location = None

    def add_beacon_point(self, position: Point3D):
        self.beacons.add(position)

    def add_beacon(self, x: int, y: int, z: int):
        self.beacons.add(Point3D(x, y, z))

    def add_beacons(self, other):
        for beacon in other.beacons:
            self.add_beacon_point(beacon + other.location)

    def inc_roll(self):
        self.roll = (self.roll + 1) % 4
        for beacon in self.beacons:
            beacon.x, beacon.y = beacon.y, -beacon.x

    def inc_yaw(self):
        self.yaw = (self.yaw + 1) % 4
        for beacon in self.beacons:
            beacon.x, beacon.output = beacon.output, -beacon.x

    def inc_pitch(self):
        self.pitch = (self.pitch + 1) % 4
        for beacon in self.beacons:
            beacon.y, beacon.output = -beacon.output, beacon.y

    def set_location(self, location: Point3D, relative_to=None):
        absolute_location = location
        if relative_to is not None and relative_to.location is not None:
            absolute_location = relative_to.location + location

        self.location = absolute_location

    def distance(self, other):
        return self.location.distance(other.location)

    def __str__(self):
        return f'Scanner {self.index}: location: {self.location}, {len(self.beacons)} beacons'

    def __repr__(self):
        return self.__str__()


def compare_scanners(scanners: []):
    base = 0
    count = 1
    while count < len(scanners):
        for i in range(1, len(scanners)):
            if i == base or scanners[base].location is None or scanners[i].location is not None:
                continue
            if compare_rotations(scanners[base], scanners[i]):
                count += 1
        base = (base + 1) % len(scanners)

    # for i in range(0, len(scanners)):
    #     for j in range(1, len(scanners)):
    #         if i == j or scanners[i].location is None:
    #             continue
    #         compare_rotations(scanners[i], scanners[j])


def compare_rotations(scanner1: Scanner, scanner2: Scanner):
    # print(f'Comparing scanners {scanner1.index} and {scanner2.index}')
    for yaw in range(0, 4):
        scanner2.inc_yaw()
        for roll in range(0, 4):
            scanner2.inc_roll()
            if compare(scanner1, scanner2):
                return True
    for pitch in range(0, 2):
        scanner2.inc_pitch()
        for roll in range(0, 4):
            scanner2.inc_roll()
            if compare(scanner1, scanner2):
                return True
        scanner2.inc_pitch()
    return False


def compare(scanner1: Scanner, scanner2: Scanner):
    results = {}
    for beacon1 in scanner1.beacons:
        for beacon2 in scanner2.beacons:
            result = beacon1 - beacon2
            if result not in results:
                results[result] = []
            results[result].append(beacon1)
            if len(results[result]) >= 12:
                scanner2.set_location(result, scanner1)
                return True

    # for k, v in results.items():
    #     if len(v) >= 12:
    #         print(
    #             f'Found: {len(v)} overlaps at point{k}, Pitch: {scanner2.pitch}, Roll: {scanner2.roll}, Yaw: {scanner2.yaw}')
    #         print(
    #             f'Setting location of scanner {scanner2.index} to {k} relative to scanner {scanner1.index} location: {scanner1.location}')
    #         scanner2.set_location(k, scanner1)
    #         return True
    return False


if __name__ == '__main__':
    scanners = input.read_scanners(from_file=False, filename='day19test1.txt')
    print(scanners)
    # 686,422,578 - -618,-824,-621 = (1304, 1246, 1199)


    # 22 (3499, 3664, 41)
    # 29 (3504, 1269, -1287)
    # print(compare_rotations(scanners[1], scanners[4]))
    print(compare_scanners(scanners))
    for s in scanners:
        print(s)
    # Scanner 0: location: (0, 0, 0), 25 beacons
    # Scanner 1: location: (68, -1246, -43), 25 beacons
    # Scanner 2: location: (1105, -1205, 1229), 26 beacons
    # Scanner 3: location: (-92, -2380, -20), 25 beacons
    # Scanner 4: location: (-20, -1133, 1061), 26 beacons
    for scanner in scanners:
        scanners[0].add_beacons(scanner)
    print(len(scanners[0].beacons))
    # part 1 answer = 378

    # part 2 answer = 13148
    maxd = 0
    for scanner1 in scanners:
        for scanner2 in scanners:
            distance = scanner1.distance(scanner2)
            if distance > maxd:
                print(f'Scanner {scanner1.index} to {scanner2.index} = {distance}')
            maxd = max(maxd, distance)
    print(maxd)
