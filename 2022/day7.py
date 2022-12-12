import input
import re

class Directory:

    def __init__(self, source, name='/', parent=None):
        self.name = name
        self.parent = parent
        self.files = []
        self.subdirs = []
        self.source = source

    def __len__(self):
        size = sum([int(file[1]) for file in self.files])
        size += sum([len(subdir) for subdir in self.subdirs])
        return size

    def parse(self):
        # first entry always "cd /"
        self.parse_remainder(self.source)

    def parse_remainder(self, remainder: list[str]):
        remainder = self.parse_listing(remainder)
        if len(remainder) < 1:
            return
        command = remainder[0]
        if command.startswith('$ cd'):
            target = command[5:]
            print(f'Changing dir to {target}')
            if target == '..':
                print(f'cd to parent {self.parent.name}')
                self.parent.parse_remainder(remainder[1:])
            else:
                print(f'Creating dir {target} under {self.name}')
                new_subdir = Directory(remainder[1:], target, self)
                self.subdirs.append(new_subdir)
                new_subdir.parse()
                # sd = next(subdir for subdir in self.subdirs if subdir.name == target)
                # print(f'cd to {sd}')
                # sd.parse_remainder(command[1:])
        elif command.startswith('$ ls'):
            print('Listing...')
            self.parse_remainder(remainder[1:])

    def parse_listing(self, remainder: list[str]):
        while len(remainder) > 0 and not remainder[0].startswith('$'):
            # ignore dir commands, no need to create dirs unless we cd into them
            if not remainder[0].startswith('dir'):
                result = re.search('([0-9]*) ([a-zA-z.]*)', remainder[0])
                print(f'Adding file: {result[2]} with size {result[1]} to dir {self.name}')
                self.files.append((result[2], result[1]))
            remainder = remainder[1:]
        return remainder

    def depth(self):
        if self.parent is None:
            return 0
        else:
            return 1 + self.parent.depth()

    def __str__(self):
        indent = '  ' * self.depth()
        result = f'{self.name} (size: {len(self)})'
        for file in self.files:
            result += f'\n{indent}  - {file[0]}: {file[1]}'
        for subdir in self.subdirs:
            result += f'\n{indent}  - {str(subdir)}'
        return result


def total_sizes(target: Directory, max_size):
    size = 0
    if len(target) < max_size:
        size += len(target)
    for subdir in target.subdirs:
        size += total_sizes(subdir, max_size)
    return size


def find_candidate(target: Directory, deletion_target, candidate=9999999999999999):
    dir_size = len(target)
    if deletion_target < dir_size < candidate:
        candidate = dir_size
        print(f'New candidate: {candidate}')
    for subdir in target.subdirs:
        candidate = min(candidate, find_candidate(subdir, deletion_target, candidate))
    return candidate


if __name__ == '__main__':
    #commands = input.read_strings(7, year=2022, from_file=True, filename='2022/day7test.txt')
    commands = input.read_strings(7, year=2022)
    print(*commands, sep='\n')
    newdir = Directory(commands[1:])
    newdir.parse()
    print(newdir)
    print(f'Total under 100,000: {total_sizes(newdir, 100000)}')
    deletion_target = len(newdir) - 40000000
    print(f'Deletion target: {deletion_target}')
    print(f'Delete candidate: {find_candidate(newdir, deletion_target)}')
