import logging


def test_iso_array_iteration():

    def diagonal_iter(start_x: int, start_y: int, width: int):
        for i in range(width):
            yield i, start_x + i, start_y + i

    def diagonal_box_iter(start_x: int, start_y: int, width: int, height: int):
        for j in range(height):
            if j > 0:
                if j % 2 == 0:
                    start_x -= 1
                else:
                    start_y += 1

            for i, x, y in diagonal_iter(start_x, start_y, width):
                yield i, j, x, y

    size_x, size_y = (10, 10)

    arr = [
        [x + (y * size_x) for x in range(size_x)]
        for y in range(size_y)
    ]
    
    buff = ''
    for lx, ly, x, y in diagonal_box_iter(3, 1, 5, 4):
        if lx == 0:
            buff += '\n'

        buff += f'({x}, {y}), '

    logging.info(buff)
            
