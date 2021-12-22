import datetime
import input
import regex as re


def rule_frequencies(chain: str, template: dict):
    return {entry: len(re.findall(f'(?={entry})', chain)) for entry in template.keys()}


def map_chars(input: str):
    return {c: input.count(c) for c in input}


def step_forward(template: dict, frequencies: dict, char_count: dict, steps: int):
    for _ in range(steps):
        for key, sub, hits in [(k, template[k], hits) for k, hits in frequencies.items() if hits > 0]:
            frequencies[f'{key[0]}{sub}'] += hits
            frequencies[f'{sub}{key[1]}'] += hits
            frequencies[key] -= hits
            char_count[sub] = char_count.setdefault(sub, 0) + hits


def solve(chain: str, template: dict, steps: int):
    frequencies = rule_frequencies(chain, template)
    char_count = map_chars(chain)
    step_forward(template, frequencies, char_count, steps)
    return max(char_count.values()) - min(char_count.values())


if __name__ == '__main__':
    _steps = 40
    _chain, _template = input.read_polymer(from_file=False, filename='day14test1.txt')
    ts = datetime.datetime.now().microsecond
    print(solve(_chain, _template, _steps))
    print(f'Elapsed: {(datetime.datetime.now().microsecond - ts) / 1000}ms')
    # 10 steps test = 1588
    # 40 steps test = 2188189693529
    # 10 steps real = 3697
    # 40 steps real = 4371307836157
