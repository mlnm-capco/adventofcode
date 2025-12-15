import math
from collections import deque
import numpy as np
from scipy.optimize import linprog
import itertools

import input


class Machine:

    def __init__(self, lights: str, buttons: list[set[int]], joltages: list[int]):
        self.lights = lights
        self.buttons = buttons
        self.joltages = joltages
        self.state = ['.'] * len(lights)

    def __repr__(self):
        return f'Machine(lights={self.lights}, buttons={self.buttons}, joltages={self.joltages})'

    def press_button(self, button_index: int):
        if button_index < 0 or button_index >= len(self.buttons):
            raise IndexError(f'Button index {button_index} out of range.')

        for light_index in self.buttons[button_index]:
            # Toggle the light
            self.state[light_index] = '#' if self.state[light_index] == '.' else '.'

    def reset(self):
        self.state = ['.'] * len(self.lights)

    def test_buttons(self, button_indices: list[int]):
        for button_index in button_indices:
            self.press_button(button_index)
        activated = self.is_activated()
        self.reset()
        return activated

    def test_buttons_joltage(self, presses: list[int]) -> tuple[bool, bool]:
        # result = [countOf([b for p in presses for b in self.buttons[p]], i) for i in range(len(self.buttons))]
        result = [0] * len(self.joltages)
        for i in range(len(presses)):
            if presses[i] == 0:
                continue
            for index in self.buttons[i]:
                result[index] += presses[i]
                if result[index] > self.joltages[index]:
                    return False, True

        return result == self.joltages, False

    def is_activated(self):
        return self.lights == ''.join(self.state)


def part_one(machines: list[Machine]):
    total = 0
    for m in machines:
        total += solve_machine(m)
    print(f'Total: {total}')
    return total

def solve_machine(machine: Machine):
    queue = deque()
    queue.extend([[i] for i in range(len(machine.buttons))])
    print(queue)
    while buttons := queue.popleft():
        if machine.test_buttons(buttons):
            print(f'Solved machine {machine} with buttons {buttons}')
            return len(buttons)
        queue.extend([*buttons, i] for i in range(len(machine.buttons)))

    return 0

def all_solutions_equation_dict(equations: dict[tuple[int], int], max_value: int = 10):
    # Find all variable indices
    all_vars = sorted(set(v for key in equations for v in key))
    n_var = len(all_vars)
    var_index = {v: i for i, v in enumerate(all_vars)}
    solution = []
    # Generate all possible assignments (0..max_value for each variable)
    min_solution = math.inf
    for candidate in itertools.product(range(max_value + 1), repeat=n_var):
        valid = True
        for key, result in equations.items():
            if sum(candidate[var_index[v]] for v in key) != result:
                valid = False
                break
        if valid and sum(candidate) < min_solution:
            solution = list(candidate)
            min_solution = sum(candidate)
    return solution

def solve_equation_dict(equations: dict[tuple[int], int]):
    # Find all variable indices
    all_vars = set()
    for key in equations:
        all_vars.update(key)
    var_list = sorted(all_vars)
    var_index = {v: i for i, v in enumerate(var_list)}
    n_eq = len(equations)
    n_var = len(var_list)
    A = np.zeros((n_eq, n_var), dtype=int)
    b = np.zeros(n_eq, dtype=int)
    for row, (vars_tuple, result) in enumerate(equations.items()):
        for v in vars_tuple:
            A[row, var_index[v]] = 1
        b[row] = result
    # Objective: minimize sum of variables
    c = np.ones(n_var)
    # Bounds: variables >= 0
    bounds = [(0, None)] * n_var
    # Use linprog to minimize sum subject to constraints
    result = linprog(c, A_eq=A, b_eq=b, bounds=bounds, method='highs')
    if result.success and np.allclose(result.x, np.round(result.x)):
        x = np.round(result.x).astype(int)
        return [int(x) for x in result.x]
    return None

def solve_machine_joltage2(machine: Machine):
    equations = {}
    for i in range(len(machine.joltages)):
        buttons = set()
        for j in range(len(machine.buttons)):
            if i in machine.buttons[j]:
                buttons.add(j)
        equations[tuple(buttons)] = machine.joltages[i]
    print(f'Equations: {equations}')

    # solve the simultaneous equations
    import numpy as np

    # Build coefficient matrix A and target vector b
    # Each row represents one light's equation
    num_lights = len(machine.joltages)
    num_buttons = len(machine.buttons)
    A = np.zeros((num_lights, num_buttons))
    b = np.array(machine.joltages)

    # Fill coefficient matrix: A[i][j] = 1 if button j affects light i
    for button_idx in range(num_buttons):
        for light_idx in machine.buttons[button_idx]:
            A[light_idx][button_idx] = 1

    # Solve the system Ax = b for non-negative integer solutions
    try:
        from scipy.optimize import linprog
        # Minimize sum of button presses: min c^T x where c = [1, 1, ..., 1]
        c = np.ones(num_buttons)
        # Equality constraint: Ax = b
        result = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method='highs', integrality=1)
        if result.success:
            presses = [int(x) for x in result.x]
        else:
            presses = [0] * num_buttons
    except np.linalg.LinAlgError:
        presses = [0] * num_buttons

    equation_dict = all_solutions_equation_dict(equations)
    print(equation_dict)
    print(f'Solved machine {machine} with {sum(presses)} presses {presses}')
    # if equation_dict is not None and equation_dict != presses:
    #     print(f"Mismatch: {equation_dict} : {presses} - {sum(equation_dict)}:{sum(presses)}")
    #     # exit(1)
    return sum(equation_dict)
    return sum(presses)

def solve_machine_joltages(machine: Machine):
    queue = deque()
    queue.append([0] * len(machine.buttons))
    while presses := queue.popleft():
        solved, overloaded = machine.test_buttons_joltage(presses)
        if solved:
            print(f'Solved machine {machine} with presses {presses}')
            return sum(presses)
        if not overloaded:
            for i in range(len(presses)):
                new_presses = presses.copy()
                new_presses[i] += 1
                queue.append(new_presses)

    return 0

def part_two(machines: list[Machine]):
    total = 0
    for m in machines:
        joltage_ = solve_machine_joltage2(m)
        if joltage_ < 1:
            print(f'Could not solve machine {m}')
            exit(1)
        total += joltage_
        print(total)
    print(f'Machines:{len(machines)} Total: {total}')
    return total



def parse_input(input_list):
    import re
    machines = []
    for line in input_list:
        match = re.match(r'^\[([.#]+)]\s+((?:\([\d,]+\)\s*)+)\{([\d,]+)}$', line.strip())

        if match:
            lights = match.group(1)  # String from []
            buttons = [set(map(int, t.split(','))) if ',' in t else {int(t)}
                     for t in re.findall(r'\(([^)]+)\)', match.group(2))]
            joltages = list(map(int, match.group(3).split(',')))
            machines.append(Machine(lights, buttons, joltages))

    return machines

# part one = 390
# part two = 14677
if __name__ == '__main__':

    day = 10
    expected1, expected2 = 7, 33

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
    # start = timer()
    parsed_real_input = parse_input(real_input)
    # real_result = part_one(parsed_real_input)
    # print(f'Part 1: {real_result}')
    # print(f'Time: {timer() - start}')

    # Real part 2
    start = timer()
    result2 = part_two(parsed_real_input)
    print(f'Part 2: {result2}')
    print(f'Time: {timer() - start}')
