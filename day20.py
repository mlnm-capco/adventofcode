import input


def enhance(enhancement: str, image: list, step: int = 1, window: int = 3):
    output = []
    total_lit = 0
    margin = 2
    for y in range(-margin, len(image) + margin):
        output_row = ''
        for x in range(-margin, len(image[0]) + margin):
            grid: str = get_grid(image, x, y, step % 2 == 0)
            result = int(grid.replace('.', '0').replace('#', '1'), 2)
            # print(f'Window: {grid}, Result: {result}, enhancement: {enhancement[result]}')
            output_row += enhancement[result]
        total_lit += output_row.count('#')
        output.append(output_row)
    return output


def get_grid(image: list, x: int, y: int, flashed: bool = False) -> str:
    grid = ''
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if i < 0 or i >= len(image[0]) or j < 0 or j >= len(image):
                grid += '#' if flashed else '.'
                continue
            grid += image[j][i]
    assert len(grid) == 9
    return grid


def print_image(image: list):
    for row in image:
        print(''.join(row))
    print(f'Dims: {len(image[0]), len(image)}, Lit: {count_lit(image)}')


def count_lit(image: list):
    total = 0
    for row in image:
        total += row.count('#')
    return total


if __name__ == '__main__':
    # #..#.
    # #....
    # ##..#
    # ..#..
    # ..###
    enhancement, image = input.read_image_data(from_file=False, filename='day20test1.txt')
    print(enhancement)
    print_image(image)
    steps = 50
    for i in range(0, steps):
        print(i)
        image = enhance(enhancement, image, step=i + 1)
        print_image(image)

    # 5339
