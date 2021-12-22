import math

import input
import regex as re


def to_binary(hex: str):
    hexint = int(f'0x{hex}', 16)
    return f'{hexint:b}'.zfill(len(hex) * 4)


class Packet:

    def __init__(self, binary: str):
        print(f'Parsing {binary}')
        self.value = 0
        self.length = 0
        self.length_indicator = None
        self.binary = binary
        self.subpackets = []
        self.parse2()

    def parse(self):
        packet_regex = '([01]{3})([01]{3})([01]*)'
        match = re.match(packet_regex, self.binary)
        self.version = int(match.group(1), 2)
        self.type = int(match.group(2), 2)
        self.literal = self.type == 4
        self.payload = match.group(3)
        self.remainder = self.payload
        self.parse_payload()

    def parse2(self):
        regx = "([01]{3})(?|(100)()()((?>1[01]{4})+0[01]{4})0*|([01]{3})(0)([01]{15})([01]*)|([01]{3})(1)([01]{11})([01]*))"
        match = re.match(regx, self.binary)
        self.version = int(match.group(1), 2)
        self.type = int(match.group(2), 2)
        self.literal = self.type == 4
        self.length_indicator = match.group(3)
        self.length = int(match.group(4), 2) if len(match.group(4)) > 0 else 0
        self.payload = match.group(5)
        if self.literal:
            self.value = sum([int(val[1:5], 2) for val in re.findall('[01]{5}', self.payload)])
            self.remainder = ''
        else:
            self.parse_operator()

    def parse_payload(self):
        if self.literal:
            self.parse_literal()
        else:
            self.parse_operator()

    def parse_operator(self):
        # self.length_indicator = self.payload[0]
        if self.length_indicator == '0':
            self.parse_operator0()
        else:
            self.parse_operator1()

    def parse_operator0(self):
        self.length = int(self.payload[1:16], 2)
        subpackets = self.payload[16:16 + self.length]
        self.remainder = self.payload[16 + self.length:]
        print(f'Parsing subpacket type 0: {subpackets}, length: {self.length}')
        i = 1
        while subpackets is not None and len(subpackets) > 0:
            subpacket = Packet(subpackets)
            # print(f'\nSubpacket {i}:\n{subpacket}')
            # print(f'Remainder: {subpacket.remainder}')
            self.subpackets.append(subpacket)
            subpackets = subpacket.remainder
            i += 1

    def parse_operator1(self):
        num_subpackets = int(self.payload[1:12], 2)
        subpackets = self.payload[12:]
        print(f'Parsing subpacket type 1: Num subs: {num_subpackets}, payload: {subpackets}')
        for _ in range(0, num_subpackets):
            subpacket = Packet(subpackets)
            self.subpackets.append(subpacket)
            subpackets = subpacket.remainder
        self.remainder = subpackets

    def parse_literal(self):
        last = False
        value = ''
        while not last:
            last = self.remainder[0] == '0'
            value += self.remainder[1:5]
            self.remainder = self.remainder[5:]
        self.value = int(value, 2)
        print(f'Parsed literal: {self.value}, version: {self.version}, remainder: {self.remainder}')
        if '1' not in self.remainder:
            self.remainder = ''

    def version_sum(self):
        return self.version + sum([p.version_sum() for p in self.subpackets])

    def calculate(self) -> int:
        if self.literal:
            return self.value
        if self.type <= 3:
            func = (sum, math.prod, min, max)[self.type]
            return func([sp.calculate() for sp in self.subpackets])
        else:
            result1 = self.subpackets[0].calculate()
            func = (result1.__gt__, result1.__lt__, result1.__eq__)[self.type - 5]
            return int(func(self.subpackets[1].calculate()))

    def __str__(self):
        return f'Version: {self.version}, ' \
               f'Type: {self.type}, ' \
               f'Payload: {self.payload}, ' \
               f'Literal: {self.literal}, ' \
               f'Value: {self.value}, ' \
               f'Length: {self.length}, ' \
               f'Length indicator: {self.length_indicator}, '  \
               f'Subpackets: {len(self.subpackets)}\n' \
               '  \n'.join(map(str, self.subpackets))

    def __repr__(self):
        return self.__str__()

class LiteralPacket(Packet):

    def parse_payload(self):
        last = False
        remaining = self.payload
        value = ''
        while not last:
            last = remaining[0] == '0'
            value += remaining[1:5]
            remaining = remaining[5:]
        self.value = int(value, 2)


def process(hex: str):
    binary = to_binary(hex)
    print(f'Processing {hex}: {binary}')
    packet = Packet(binary)
    print(packet)
    print(f'Version sum: {packet.version_sum()}')
    print(f'Calculation: {packet.calculate()}')

    print()
    return packet


if __name__ == '__main__':
    # hex = input.read_strings(16, False, 'day18test1.txt')[0]
    # process(hex)
    # process('D2FE28')  # literal = 2021
    process('38006F45291200') # operator(literal=10, literal=20)
    # process('EE00D40C823060')  # operator(3 literal subs)

    # process('8A004A801A8002F478')  # 16
    # process('620080001611562C8802118E34')  # 12
    # process('C0015000016115A2E0802F182340')  # 23

    # part 2 = 9485076995911
    # C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
    # process('C200B40A82')
    # 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
    # process('04005AC33890')
    # 880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
    # process('880086C3E88112')
    # CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
    # process('CE00C43D881120')
    # D8005AC2A8F0 produces 1, because 5 is less than 15.
    # process('D8005AC2A8F0')
    # F600BC2D8F produces 0, because 5 is not greater than 15.
    # process('F600BC2D8F')
    # 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
    # process('9C005AC2F8F0')
    # 9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
    # process('9C0141080250320F1802104A08')

    # regx = "([01]{3})(?|(100)()()((?>1[01]{4})+0[01]{4})0*|([01]{3})(0)([01]{15})([01]*)|([01]{3})(1)([01]{11})([01]*))"
    # match = re.match(regx, '0001001001000110011100011010000')
    # for i in range(0, 6):
    #     print(i, match.group(i))
    # print(re.findall('[01]{5}', match.group(5)))
    #
    # match = re.match(regx, '11001100000000011010100010001001000100111110000111100001100000000011000100001111101000110010010001100')
    # for i in range(0, 6):
    #     print(i, match.group(i))
