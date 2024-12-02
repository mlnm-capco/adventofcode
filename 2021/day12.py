import input


def count_paths(graph, start: str, visited=None, double_visited=False):
    if visited is None:
        visited = list()
    # print(f'Checking {visited} + {start}')
    if start == 'end':
        print(f'**** Found path: {"-".join(visited)}-{start}')
        return 1
    if start not in graph:
        print(f'**Dead end: {"-".join(visited)}-{start}')
        return 0
    if start.islower() and start in visited:
        if start in ['start', 'end'] or double_visited:
            print(f'**Already visited: {"-".join(visited)}-{start}')
            return 0
        else:
            double_visited = True
    visited.append(start)
    return sum([count_paths(graph, node, visited[:], double_visited) for node in graph[start]])


if __name__ == '__main__':
    graph = input.read_graph(from_file=False, filename='day12test3.txt')
    # paths[node] = sum[paths[next] for next in child_nodes]
    print(graph)
    # part 1
    print(count_paths(graph, 'start', double_visited=True))  # 5333
    # part 2
    print(count_paths(graph, 'start'))  # 146553

