
class Digitmapper:

    bitmaps = [0b1110111,
               0b0010010,
               0b1011101,
               0b1011011,
               0b0111010,
               0b1101011,
               0b1101111,
               0b1010010,
               0b1111111,
               0b1111011]

    def __init__(self):
        self.knowns: [str] = [None] * 10
        self.unknowns: [str] = []

    def map_digits(self, strings: [str]):
        for digit in strings:
            self.deduce(digit)

    def parse_string(self, strings: [str]):
        return [self.knowns.index(''.join(sorted(value.strip()))) for value in strings]

    def process_digit(self, digit: str):
        result = self.deduce(digit)
        if result >= 0:
            self.knowns[result] = digit
        else:
            self.unknowns.append(digit)
        print(f'{digit} = {result}')
        return result

    def get_possible_values(self, digit: str):
        return [i for i, bitmap in enumerate(self.bitmaps) if f'{bitmap:07b}'.count('1') == len(digit)]

    def deduce(self, digit: str):
        possible_values = self.get_possible_values(digit)
        if len(possible_values) > 1:
            possible_values[:] = [candidate for candidate in possible_values if self.is_viable(candidate, digit, possible_values)]

        if len(possible_values) == 1:
            self.knowns[possible_values[0]] = ''.join(sorted(digit))
            self.recheck_unknowns()
            return possible_values[0]
        return -1

    def is_viable(self, candidate, digit, possible_values):
        if self.knowns[candidate] is not None:  # already known
            return False
        else:
            for known_digit, known_string in enumerate(self.knowns):
                if known_string is None:
                    continue
                intersect = len([c for c in digit if known_string is not None and c in known_string])
                xor = f'{Digitmapper.bitmaps[candidate] & Digitmapper.bitmaps[known_digit]:07b}'.count('1')
                if xor != intersect:
                    return False
        return True

    def recheck_unknowns(self):
        for unknown in self.unknowns:
            self.deduce(unknown)


if __name__ == '__main__':
    mapper = Digitmapper()
    mapper.process_digit('acdeg')  # 2
    mapper.process_digit('abcdfg')  # 9
    mapper.process_digit('acdfg')  # 3
    mapper.process_digit('abdfg')  # 5
    mapper.process_digit('acf')  # 7
    mapper.process_digit('abdefg')  # 6
    mapper.process_digit('abcefg')  # 0
    mapper.process_digit("cf")  # 1
    mapper.process_digit('abcdefg')  # 8
    mapper.process_digit('bcdf')  # 4
    print(mapper.knowns)
    mapper.map_positions()
    print(f'{mapper.top}, {mapper.tl}, {mapper.tr}, {mapper.mid}, {mapper.bl}, {mapper.br}, {mapper.bottom}')
    print(mapper.parse_string(['dfcb', 'gabdcfe', 'fc']))
    # print(mapper.intersection_of([0, 2, 3, 5, 6, 7]))
    # print(mapper.intersection_of([0, 4, 5, 6, 8, 9]))
    # print(mapper.intersection_of([1, 2]))
    # print(mapper.intersection_of([1, 5]))
    # print(mapper.intersection_of([4, 2, 5]))
    # print(mapper.difference_of([4, 3]))
    # print(mapper.difference_of([2, 3]))
    # print(mapper.difference_of([3, 4, 7]))

