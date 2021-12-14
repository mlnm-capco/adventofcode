import input
import regex as re


def hit_count(chain: str, template: dict):
    return {entry: len(re.findall(f'(?={entry})', chain)) for entry in template.keys()}


def str_to_dict(input: str):
    return {c: input.count(c) for c in input}


def step_forward(template: dict, hitcount: dict, char_count: dict, steps: int):
    for _ in range(steps):
        for key, sub, hits in [(k, template[k], hits) for k, hits in hitcount.items() if hits > 0]:
            hitcount[f'{key[0]}{sub}'] += hits
            hitcount[f'{sub}{key[1]}'] += hits
            hitcount[key] -= hits
            char_count[sub] = char_count.setdefault(sub, 0) + hits


def solve(chain: str, template: dict, steps: int):
    hitmap = hit_count(chain, template)
    char_count = str_to_dict(chain)
    step_forward(template, hitmap, char_count, steps)
    return max(char_count.values()) - min(char_count.values())


if __name__ == '__main__':
    _steps = 40
    _chain, _template = input.read_polymer(from_file=True, filename='day14test1.txt')

    print(solve(_chain, _template, _steps))

    # 10 steps test = 1588
    # 40 steps test = 2188189693529
    # 10 steps real = 3697
    # 40 steps real = 4371307836157
