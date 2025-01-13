import input


def part_one(network: dict):
    results= set()
    for node, connections in network.items():
        if not str(node).startswith('t'):
            continue
        for connection in connections:
            if not connection in network:
                continue
            connection_connections = network[connection]
            for c2 in connection_connections:
                if c2 != node and c2 != connection and node in connection_connections and node in network[c2]:
                    results.add(tuple(sorted(([node, connection, c2]))))
    print(f'Part one results: {results}')
    return len(results)


def part_two(network: dict):
    R, X, P = set(), set(), set(network.keys())
    return ','.join(sorted(bron_kerbosch1(network, R, P, X)))


def bron_kerbosch1(network: dict, R: set, P: set, X: set):
    if len(P) == 0 and len(X) == 0:
        return R

    max_clique = set()
    for vertex in P.union(set([])):
        neighbours = network[vertex]
        result = bron_kerbosch1(network, R.union({vertex}), P.intersection(neighbours), X.intersection(neighbours))
        if len(result) > len(max_clique):
            max_clique = result
        P.remove(vertex)
        X.add(vertex)
    return max_clique

# part one = 1075
# part two = az,cg,ei,hz,jc,km,kt,mv,sv,sx,wc,wq,xy
if __name__ == '__main__':

    day = 23
    expected1, expected2 = 7, 'co,de,ka,ta'

    test_input = input.read_graph(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')
    print(f'Test input: \n{test_input}')

    # Test part 1
    test_result = part_one(test_input)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    test_result2 = part_two(test_input)
    print(f'Part 2 test: {test_result2}')
    assert test_result2 == expected2

    real_input = input.read_graph(day, year=2024, from_file=False)
    print(f'Real input: \n{real_input}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    real_result = part_one(real_input)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')


