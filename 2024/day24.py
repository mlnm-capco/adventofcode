import math
from collections import deque

import regex

import input

class Gate:

    def __init__(self, input1, op, input2, output):
        self.input_wire1, self.input_wire2, self.op, self.output_wire = input1, input2, op, output
        self.input1_value, self.input2_value, self.output_value = None, None, None

    def __repr__(self):
        return f'{self.input_wire1} {self.op} {self.input_wire2} => {self.output_wire}'

    def process(self, in1, in2):
        self.input1_value, self.input2_value = in1, in2
        if self.op == 'AND':
            self.output_value = in1 & in2
        elif self.op == 'OR':
            self.output_value =  in1 | in2
        else:
            self.output_value = in1 ^ in2
        return self.output_value

def part_one(wires: dict, gates: list[Gate]):
    return run(wires, gates)

def run(wires: dict, gates: list[Gate]):
    z_wires = sum(k.startswith('z') for k in wires.keys() if k.startswith('z'))
    z_count = 0
    print(f'Z wires: {z_wires}')
    while z_count < z_wires:
        for gate in gates:
            input1, input2 = gate.input_wire1, gate.input_wire2
            if input1 in wires and wires[input1] is not None and input2 in wires and wires[input2] is not None:
                result = gate.process(wires[input1], wires[input2])
                if wires[gate.output_wire] is None:
                    wires[gate.output_wire] = result
                    if gate.output_wire.startswith('z'):
                        z_count = z_count + 1
    z_results = dict(sorted({k: v for k, v in wires.items() if k.startswith("z")}.items()))
    print(f'z wires: {z_results}')
    answer = sum([2 ** int(k[1:3]) for k, v in z_results.items() if v])
    return answer

def part_two(wires: dict, gates: list[Gate]):
    x = sum([2 ** int(k[1:3]) for k, v in wires.items() if k.startswith('x') and v])
    y = sum([2 ** int(k[1:3]) for k, v in wires.items() if k.startswith('y') and v])
    z = run(wires, gates)
    print(f'X: {x}, Y: {y}, target result = {x + y}')
    print(f'X: {bin(x)}, Y: {bin(y)}, target result = {bin(x + y)}')
    difference = z ^ (x + y)
    print(f'Difference: {difference}')
    print(f'Target:     {bin(x + y)}')
    print(f'Actual:     {bin(z)}')
    print(f'Difference: {bin(difference)}')
    incorrect_z_bits = set()
    for i in range(0, int(math.log2(difference) + 1)):
        if (2 ** i) & difference:
            incorrect_z_bits.add(i)
    print(f'Incorrect Z bits: {incorrect_z_bits}')
    candidates = {f'z{str(bit).rjust(2, "0")}' for bit in incorrect_z_bits}
    incorrect_outputs = deque(candidates)
    print(incorrect_outputs)

    candidate_map = dict()
    for z_candidate in candidates:
        candidate_map[z_candidate] = set()
        incorrect_outputs = deque([z_candidate])
        while len(incorrect_outputs) > 0:
            incorrect_output = incorrect_outputs.pop()
            if incorrect_output.startswith('x') or incorrect_output.startswith('y'):
                continue
            actual = wires[incorrect_output]
            for g in gates:
                if g.output_wire == incorrect_output:
                    candidate_map[z_candidate].add(incorrect_output)
                    if g.op == 'AND':
                        if wires[g.input_wire1] == actual:
                            incorrect_outputs.append(g.input_wire1)
                        if wires[g.input_wire2] == actual:
                            incorrect_outputs.append(g.input_wire2)
                    elif g.op == 'OR':
                        if wires[g.input_wire1] != actual:
                            incorrect_outputs.append(g.input_wire1)
                        if wires[g.input_wire2] != actual:
                            incorrect_outputs.append(g.input_wire2)
                    elif g.op == 'XOR':
                        incorrect_outputs.append(g.input_wire1)
                        incorrect_outputs.append(g.input_wire2)
        print(f'Candidates for {z_candidate}: {[f"{s}: {wires[s]}" for s in candidate_map[z_candidate]]} ({len(candidate_map[z_candidate])})')


def try_candidates(gates: list[Gate], wires, candidate_map: dict):
    gates_by_output = {g.output_wire: g for g in gates}
    for z_candidates1 in candidate_map:
        for z_candidates2 in candidate_map:
            if z_candidates1 == z_candidates2:
                continue
            for candidates1 in z_candidates1:
                for candidates2 in z_candidates2:
                    if wires[candidates1] != wires[candidates2]:
                        out1 = gates_by_output[candidates1].output_wire
                        gates_by_output[candidates1].output_wire = gates_by_output[candidates2].output_wire
                        gates_by_output[candidates2].output_wire = out1

def try_gates(gates, wires):
    reset_wires(wires)
    run(wires, gates)

def calculate_incorrect_bits():

    # for g1 in gates:
    #     for g2 in gates:
    #         if g1.output_wire == g2.output_wire:
    #             continue

    return NotImplemented

def reset_wires(wires: dict):
    for k, v in wires.items():
        if k[0] != 'x' and k[0] != 'y':
            wires[k] = None

# y04: 1
#
# ntg XOR fgs -> mjb
def parse_input(input):
    wires = dict()
    gates = []
    i = 0
    for line in input:
        if len(line.strip()) == 0:
            break
        name, value = line.split(':')
        wires[name.strip()] = bool(int(value.strip()))
        i += 1
    for line in input[i + 1: ]:
        match = regex.match('(.*) (OR|AND|XOR) (.*) -> (.*)', line)
        if match is not None:
            wire_in1, op, wire_in2, wire_out = match.group(1), match.group(2), match.group(3), match.group(4)
            gates.append(Gate(wire_in1, op, wire_in2, wire_out))
            if wire_out not in wires:
                wires[wire_out] = None
    return wires, gates

# part one = 1073742054 too low
# part two = btb,cmv,mwp,rdg,rmj,z17,z23,z30
# btb,*cmv*,*mwp*,rdg,rmj,*z17*,*z23*,z30
#Candidates for z26: ['mnf: False', 'z26: False', 'bmw: True', 'dwn: True'] (4)
# Candidates for z25: ['z25: False', 'vjw: False', 'nhb: True', 'tcr: True'] (4)
# Candidates for z28: ['z28: True', 'vvc: False', 'kdt: False', 'kgr: True'] (4)
# Candidates for z27: ['cpc: True', 'jpd: False', 'z27: False', 'ktr: True'] (4)
# Candidates for z19: ['drf: True', 'z19: False', 'ksj: False', 'mtd: True'] (4)
# Candidates for z17: ['***z17***: False'] (1)
# Candidates for z24: ['frg: False', 'hqn: True', 'pkh: True', 'z24: False'] (4)
# Candidates for z18: ['wvj: True', 'fwm: True', 'z18: False', '***cmv***: True', 'qwg: False'] (5)
# Candidates for z38: ['bqj: False', 'tsk: True', '***mwp***: False', 'z38: True'] (4)
# Candidates for z23: ['***z23***: False', 'kkf: False'] (2)
# Candidates for z20: ['z20: True', 'sgm: False', 'ckr: False', 'dmf: True'] (4)
if __name__ == '__main__':

    day = 24
    expected1, expected2 = 2024, -1

    test_input = input.read_strings(day, year=2024, from_file=True, filename=f'../input/2024/day{day}test.txt')
    print(f'Test input: \n{test_input}')
    wires, gates = parse_input(test_input)
    print(f'Test: Wires: {wires}\nGates: {gates}')

    # Test part 1
    test_result = part_one(wires, gates)
    print(f'Part 1 test: {test_result}')
    if expected1 > -1:
        assert test_result == expected1

    # Test part 2
    wires, gates = parse_input(test_input)
    test_result2 = part_two(wires, gates)
    print(f'Part 2 test: {test_result2}')
    if expected2 > -1:
        assert test_result2 == expected2

    real_input = input.read_strings(day, year=2024, from_file=False)
    print(f'Real input: \n{real_input}')
    wires, gates = parse_input(real_input)
    print(f'Real: Wires: {wires}\nGates: {gates}')

    from timeit import default_timer as timer

    # Real part 1
    start = timer()
    real_result = part_one(wires, gates)
    print(f'Part 1: {real_result}')
    print(f'Time: {timer() - start}')

    # Real part 2
    wires, gates = parse_input(real_input)

    start = timer()
    result2 = part_two(wires, gates)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')


