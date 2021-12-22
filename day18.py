from enum import Enum

import input
import math


class SFNumber:

    def __init__(self, raw, parent=None):
        self.parent = parent
        self.left = self.right = self.value = None
        if raw is None or isinstance(raw, int):
            self.value = raw
            return

        sf_list = list(raw)
        assert len(sf_list) == 2
        self.left = SFNumber(sf_list[0], self)
        self.right = SFNumber(sf_list[1], self)

    def is_leaf(self):
        return self.value is not None

    def is_leaf_pair(self):
        return not self.is_leaf() and self.left.is_leaf() and self.right.is_leaf()

    def add(self, other):
        new_sfn = SFNumber(None)
        new_sfn.left = self
        new_sfn.right = other
        new_sfn.left.parent = new_sfn.right.parent = new_sfn
        return new_sfn

    def reduce(self):
        while self.do_explosions() or self.do_splits():
            continue

    def do_explosions(self):
        # print(f'Processing explosions: {self}')
        if self.is_leaf():
            return False
        if self.is_leaf_pair() and self.depth() >= 4:
            return self.explode()
        return self.left.do_explosions() or self.right.do_explosions()

    def do_splits(self):
        # print(f'Processing splits: {self}')
        if self.is_leaf():
            return self.value >= 10 and self.split()
        return self.left.do_splits() or self.right.do_splits()

    def explode(self):
        assert self.is_leaf_pair()
        # print(f'Exploding: {self}')
        if self.parent is not None:
            self.parent.propagate(self.left.value, False, [self])
            self.parent.propagate(self.right.value, True, [self])
        self.value = 0
        self.left = self.right = None
        # print(f'Exploded: {self.root()}')
        return True

    def root(self):
        if self.parent is None:
            return self
        return self.parent.root()

    def depth(self, depth: int = 0):
        if self.parent is None:
            return depth
        return self.parent.depth(depth + 1)

    def propagate(self, operand: int, left: bool, visited: list = [], backtracked: bool = False):
        forward, back = (self.left, self.right) if left else (self.right, self.left)
        visited.append(self)
        if self.is_leaf():
            if backtracked:
                self.value += operand
            return backtracked
        if backtracked and forward not in visited and forward.propagate(operand, left, visited, backtracked):
            return True
        if back not in visited and back.propagate(operand, left, visited, True):
            return True

        return False if self.parent is None else self.parent.propagate(operand, left, visited, backtracked)

    def split(self):
        # print(f'Splitting: {self}')
        if not self.is_leaf():
            raise RuntimeError('Attempting to split a non-leaf node')
        self.left = SFNumber(int(self.value / 2), self)
        self.right = SFNumber(int(math.ceil(self.value / 2)), self)
        self.value = None
        # print(f'Split: {self.root()}')
        return True

    def total(self):
        if self.is_leaf():
            return self.value
        return 3 * self.left.total() + 2 * self.right.total()

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        return f'[{self.left}, {self.right}]'

    def __repr__(self):
        return self.__str__()


def add_reduce(sf_list1: list, sf_list2: list):
    sf_number1 = SFNumber(sf_list1)
    sf_number2 = SFNumber(sf_list2)
    print(sf_number1)
    print('+')
    print(sf_number2)
    result = sf_number1.add(sf_number2)
    print(f"Added: {result}")
    result.reduce()
    print(f'Reduced: {result}')
    return result


if __name__ == '__main__':
    # [[[[4,3],4],4],[7,[[8,4],9]]]

    # [[[[4, 3], 4], 4], [7, [[8, 4], 9]]] + [1, 1]:
    #
    # after addition: [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]
    # after explode: [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]
    # after explode: [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]
    # after split: [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]
    # after split: [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]
    # after explode: [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    # add_reduce([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1,1])

    # add and reduce
    #     [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]]
    # + [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]
    # = [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]

    # add_reduce([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]], [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]])
    # exit(0)



    import ast

    # part 1
    lines = input.read_strings(18, False, 'day18test2.txt')
    # result = SFNumber(ast.literal_eval(lines[0]))
    # print(result)
    # for line in lines[1:]:
    #     sf_list = ast.literal_eval(line)
    #     sf_number = SFNumber(sf_list)
    #     print(f'Adding {sf_number}')
    #     result = result.add(sf_number)
    #     print(f'Addition result: {result}')
    #     result.reduce()
    #     print(f'Reduction result: {result}')
    #     print()
    # print(f'Result: {result}')
    # print(f'Result total: {result.total()}')

    # part 2:
    max_total = 0
    for line1 in lines:
        for line2 in lines:
            if line1 == line2:
                continue
            print(f'{line1}\n+ {line2}')
            result = add_reduce(ast.literal_eval(line1), ast.literal_eval(line2))
            max_total = max(max_total, result.total())
    print(f'Max: {max_total}')


    # part 1 result = 3806
    # test 4140
    # [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]

    # sf_list = [7, [6, [5, [4, [3, 2]]]]]  # [7, [6, [5, [7, 0]]]]
    # sf_list = [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]  # [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    #
    # sf_list = [[6, [5, [4, [3, 2]]]], 1]   # [[6, [5, [7, 0]]], 3].
    # sf_list = [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]  # [[3, [2, [8, 0]]], [9, [5, [7, 0]]]].
    #
    # sf_number = SFNumber(sf_list)
    # print(sf_number)
    # sf_number.process()

    # [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
    # sf_list = [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]  # [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
    # print(sf_number)
    # sf_number.reduce()

    # print(f'Exploding {sf_number.left.right.right.right}')
    # sf_number.left.right.right.right.explode()
    # sf_number.right.right.right.right.explode()
    # print(sf_number)
    # print(sf_number)
    # sf_number = sf_number.add(SFNumber([1, 1]))
    # print(sf_number)
    # print()
    # sflist2 = SFNumber([35, 4])
    # sflist2.left.split()
    # print(sflist2)
    # print(sflist2.total())
