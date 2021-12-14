from input import read_manual

if __name__ == '__main__':
    manual = read_manual(from_file=False, filename='day13test1.txt')
    print(manual)
    print(len(manual))
    print()
    manual.apply_folds()
    print(manual)
    print(len(manual))
