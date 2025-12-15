import math

import input
from mytypes.grid import Point, Point3D, Cuboid


def part_one(boxes: list[Point3D], iterations = 10, plot_size: int = 1000):
    neighbours, circuits = {}, []
    for box in boxes:
        closest, distance = find_closest(box, boxes)
        print(f"Box {box}: closest is {closest} at {distance}")
        neighbours[box] = (closest, distance)

    direct_connections = dict()
    for i in range(iterations):
        print(f"\n{i}: Neighbours: {neighbours}")
        closest_pair = min(neighbours.items(), key=lambda item: item[1][1])
        print(f"Closest pair: {closest_pair}")

        box1, box2 = closest_pair[0], closest_pair[1][0]
        existing_circuit, circuit_to_merge = None, None
        for circuit in circuits:
            if box1 in circuit or box2 in circuit:
                print(f'Adding {box1} and {box2} to existing circuit: {circuit}')
                circuit.add(box1)
                circuit.add(box2)
                if existing_circuit is not None:
                    circuit_to_merge = circuit
                else:
                    existing_circuit = circuit
        if circuit_to_merge is not None:
            print(f'Merging circuits: {existing_circuit} and {circuit_to_merge}')
            existing_circuit.update(circuit_to_merge)
            circuits.remove(circuit_to_merge)
        if existing_circuit is None:
            print(f'Adding {box1} and {box2} to new circuit')
            existing_circuit = {box1, box2}
            circuits.append(existing_circuit)
        # print(f'Circuits: {circuits}')
        for c in circuits: print(c)
        print(f'Circuit sizes: {[len(c) for c in circuits]}')

        if box1 not in direct_connections:
            direct_connections[box1] = set()
        if box2 not in direct_connections:
            direct_connections[box2] = set()
        direct_connections[box1].add(box2)
        direct_connections[box2].add(box1)
        print(f'Old: {box1}: {neighbours[box1]}, {box2}: {neighbours[box2]}')
        neighbours[box1] = find_closest(box1, boxes, direct_connections[box1])
        neighbours[box2] = find_closest(box2, boxes, direct_connections[box2])
        print(f'New: {box1}: {neighbours[box1]}, {box2}: {neighbours[box2]}')

    plot_boxes(boxes, direct_connections, plot_size)

    print(f'Final circuits: {circuits}')
    total = math.prod(sorted([len(c) for c in circuits], reverse=True)[:3])
    print(f'\nTotal = {total}')
    return total


def find_closest(box: Point3D, boxes: list[Point3D], circuit: set[Point3D]= None):
    closest = None, math.inf
    for candidate in boxes:
        if box == candidate or (circuit is not None and candidate in circuit):
            continue
        dist = box.euclid_distance(candidate)
        if dist < closest[1]:
            closest = candidate, dist
    return closest


def part_two(boxes: list[Point3D]):
    neighbours, circuits = {}, []
    for box in boxes:
        closest, distance = find_closest(box, boxes)
        print(f"Box {box}: closest is {closest} at {distance}")
        neighbours[box] = (closest, distance)

    while len(circuits) != 1 or (len(circuits) == 0 or len(circuits[0]) != len(boxes)):
        # print(f"\nNeighbours: {neighbours}")
        closest_pair = min(neighbours.items(), key=lambda item: item[1][1])
        print(f"\nClosest pair: {closest_pair}")

        box1, box2 = closest_pair[0], closest_pair[1][0]
        existing_circuit, circuit_to_merge = None, None
        for circuit in circuits:
            if box1 in circuit or box2 in circuit:
                circuit.add(box1)
                circuit.add(box2)
                if existing_circuit is not None:
                    circuit_to_merge = circuit
                else:
                    print(f'Adding {box1} and {box2} to existing circuit of size: {len(circuit)}')
                    existing_circuit = circuit
        if circuit_to_merge is not None:
            print(f'Merging circuits of size: {len(existing_circuit)} and {len(circuit_to_merge)}')
            existing_circuit.update(circuit_to_merge)
            circuits.remove(circuit_to_merge)
        if existing_circuit is None:
            print(f'Adding {box1} and {box2} to new circuit')
            existing_circuit = {box1, box2}
            circuits.append(existing_circuit)

        # for c in circuits: print(c)
        print(f'Circuit sizes: {[len(c) for c in circuits]}')

        if len(circuits) == 1 and len(circuits[0]) == len(boxes):
            print('\nAll boxes connected!')
            print(f'Last connection: {box1}, {box2}')
            return box1.x * box2.x

        neighbours[box1] = find_closest(box1, boxes, existing_circuit)
        neighbours[box2] = find_closest(box2, boxes, existing_circuit)

    print(f'Final circuits: {circuits}')
    return 0


def plot_boxes(boxes: list[Point3D], connections: dict[Point3D, set[Point3D]], size: int = 1000):

    cuboid = Cuboid(Point3D(0, 0,0 ), Point3D(size,size,size))
    cuboid.plot(set(boxes), connections)


def parse_input(input_list):
    return [Point3D(*map(int, line.split(','))) for line in input_list]

# part one = 50568
# part two = 36045012
if __name__ == '__main__':

    day = 8
    expected1, expected2 = 40, 25272

    test_input = input.read_strings(day, year=2025, from_file=True, test=True)
    print(f'Test input: \n{test_input}')
    parsed_test_input = parse_input(test_input)
    print(f'Parsed test input: \n{parsed_test_input}')

    # Test part 1
    test_result = part_one(parsed_test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    test_result2 = part_two(parsed_test_input)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2

    # exit(0)

    real_input = input.read_strings(day, year=2025, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    parsed_real_input = parse_input(real_input)
    real_result = part_one(parsed_real_input, 1000, 100000)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(parsed_real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
