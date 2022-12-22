import re
import sys
from enum import Enum, StrEnum
from typing import Tuple

from aoc import input_as_str_nostrip, Point, chunk

WIDTH = 0
HEIGHT = 0
CUBE_SIDE_SIZE = sys.maxsize


class Dir(StrEnum):
    RIGHT = '>',
    LEFT = '<',
    UP = '^',
    DOWN = 'v'


def get_facing_value(dir: Dir) -> int:
    if dir == Dir.RIGHT:
        return 0
    if dir == Dir.DOWN:
        return 1
    if dir == Dir.LEFT:
        return 2
    if dir == Dir.UP:
        return 3


def do_turn(cur_dir, turn) -> Dir:
    if len(turn) == 0 or turn not in 'LR':
        return cur_dir
    if cur_dir == Dir.RIGHT:
        if turn == 'L':
            return Dir.UP
        else:
            return Dir.DOWN
    if cur_dir == Dir.DOWN:
        if turn == 'L':
            return Dir.RIGHT
        else:
            return Dir.LEFT
    if cur_dir == Dir.LEFT:
        if turn == 'L':
            return Dir.DOWN
        else:
            return Dir.UP
    if cur_dir == Dir.UP:
        if turn == 'L':
            return Dir.LEFT
        else:
            return Dir.RIGHT
    return cur_dir


def parse_input(lines):
    global WIDTH, HEIGHT, CUBE_SIDE_SIZE
    grid, instructions = lines.split('\n\n')
    walls = set()
    free = set()
    min_max_line = {}
    min_max_row = {}
    for y, line in enumerate(grid.splitlines()):
        HEIGHT = max(y, HEIGHT)
        for x, c in enumerate(line):
            WIDTH = max(x, WIDTH)

            p = Point(x, y)
            if c == '#':
                add_to_min_max(min_max_line, x, y)
                add_to_min_max(min_max_row, y, x)
                walls.add(p)
            elif c == '.':
                add_to_min_max(min_max_line, x, y)
                add_to_min_max(min_max_row, y, x)
                free.add(p)
    instructions = re.split('(\d+)', instructions.strip())
    instructions.pop()
    WIDTH += 1
    HEIGHT += 1
    min_side = min(min_max_line.values(), key=lambda v: v[1] - v[0])
    CUBE_SIDE_SIZE = min_side[1] - min_side[0] + 1
    return walls, free, min_max_line, min_max_row, instructions


def add_to_min_max(min_max_line, entry, index):
    if index not in min_max_line:
        min_max_line[index] = [entry, entry]
    else:
        min_max_line[index][1] = entry


def get_next(p, dir, min_max_line, min_max_row):
    if dir == Dir.RIGHT:
        x_new = p.x + 1
        if x_new > min_max_line[p.y][1]:
            x_new = min_max_line[p.y][0]
        return dir, Point(x_new, p.y)
    if dir == Dir.DOWN:
        y_new = p.y + 1
        if y_new > min_max_row[p.x][1]:
            y_new = min_max_row[p.x][0]
        return dir, Point(p.x, y_new)
    if dir == Dir.LEFT:
        x_new = p.x - 1
        if x_new < min_max_line[p.y][0]:
            x_new = min_max_line[p.y][1]
        return dir, Point(x_new, p.y)
    if dir == Dir.UP:
        y_new = p.y - 1
        if y_new < min_max_row[p.x][0]:
            y_new = min_max_row[p.x][1]
        return dir, Point(p.x, y_new)


def get_next_real(p, dir, min_max_line, min_max_row) -> Tuple[Dir, Point]:
    if dir == Dir.RIGHT:
        x_new = p.x + 1
        # side 1
        if x_new > min_max_line[p.y][1]:
            if p.y < CUBE_SIDE_SIZE:
                return dir.LEFT, Point(99, (3 * CUBE_SIDE_SIZE - 1) - p.y)
            elif p.y < 2 * CUBE_SIDE_SIZE:
                dir = dir.UP
                return dir, Point(x=2 * CUBE_SIDE_SIZE + (p.y - CUBE_SIDE_SIZE), y=CUBE_SIDE_SIZE - 1)
            elif p.y < 3 * CUBE_SIDE_SIZE:
                dir = dir.LEFT
                return dir, Point(x=3 * CUBE_SIDE_SIZE - 1, y=(3 * CUBE_SIDE_SIZE - 1) - p.y)
            elif p.y < 4 * CUBE_SIDE_SIZE:
                dir = dir.UP
                return dir, Point(x=CUBE_SIDE_SIZE + p.y - (3 * CUBE_SIDE_SIZE), y=(3 * CUBE_SIDE_SIZE - 1))
            else:
                print("error")
        return dir, Point(x_new, p.y)
    if dir == Dir.DOWN:
        y_new = p.y + 1
        if y_new > min_max_row[p.x][1]:
            if p.x < CUBE_SIDE_SIZE:
                return dir.DOWN, Point(2 * CUBE_SIDE_SIZE + p.x, 0)
            elif p.x < 2 * CUBE_SIDE_SIZE:
                return dir.LEFT, Point(CUBE_SIDE_SIZE - 1, 3 * CUBE_SIDE_SIZE + p.x - CUBE_SIDE_SIZE)
            elif p.x < 3 * CUBE_SIDE_SIZE:
                return dir.LEFT, Point(x=2 * CUBE_SIDE_SIZE - 1, y=CUBE_SIDE_SIZE + p.x - 2 * CUBE_SIDE_SIZE)
            else:
                print("error")
        return dir, Point(p.x, y_new)
    if dir == Dir.LEFT:
        x_new = p.x - 1
        if x_new < min_max_line[p.y][0]:
            if p.y < CUBE_SIDE_SIZE:
                return dir.RIGHT, Point(0, (3 * CUBE_SIDE_SIZE - 1) - p.y)
            elif p.y < 2 * CUBE_SIDE_SIZE:
                dir = dir.DOWN
                return dir, Point(x=p.y - CUBE_SIDE_SIZE, y=2 * CUBE_SIDE_SIZE)
            elif p.y < 3 * CUBE_SIDE_SIZE:
                dir = dir.RIGHT
                return dir, Point(x=CUBE_SIDE_SIZE, y=(3 * CUBE_SIDE_SIZE - 1) - p.y)
            elif p.y < 4 * CUBE_SIDE_SIZE:
                dir = dir.DOWN
                return dir, Point(x=CUBE_SIDE_SIZE + p.y - (3 * CUBE_SIDE_SIZE), y=0)
            else:
                print("error")
        return dir, Point(x_new, p.y)
    if dir == Dir.UP:
        y_new = p.y - 1
        if y_new < min_max_row[p.x][0]:
            if p.x < CUBE_SIDE_SIZE:
                return dir.RIGHT, Point(50, CUBE_SIDE_SIZE + p.x)
            elif p.x < 2 * CUBE_SIDE_SIZE:
                return dir.RIGHT, Point(0, 3 * CUBE_SIDE_SIZE + p.x - CUBE_SIDE_SIZE)
            elif p.x < 3 * CUBE_SIDE_SIZE:
                return dir.UP, Point(p.x - 2 * CUBE_SIDE_SIZE, 4 * CUBE_SIDE_SIZE - 1)
            else:
                print("error")
        return dir, Point(p.x, y_new)


def part_1(walls, free, min_max_line, min_max_row, instructions):
    cur = Point(y=0, x=min_max_line[0][0])
    dir = Dir.RIGHT
    path = {}
    for turn, length in chunk(instructions, size=2):
        dir = do_turn(dir, turn)
        i = 0
        next = cur
        path[cur] = dir.value
        while next not in walls and i <= int(length):
            cur = next
            _, next = get_next(cur, dir, min_max_line, min_max_row)
            i += 1
    return 1000 * (cur.y + 1) + 4 * (cur.x + 1) + get_facing_value(dir)


def print_grid(free, min_max_line, min_max_row, path, walls):
    for y in range(max(min_max_line.keys())):
        for x in range(max(min_max_row.keys())):
            p = Point(x, y)
            if p in walls:
                print('#', end='')
            elif p in path:
                print(path[p], end='')
            elif p in free:
                print('.', end='')
            else:
                print(' ', end='')
        print()


def part_2(walls, free, min_max_line, min_max_row, instructions):
    tests(min_max_line, min_max_row)
    cur = Point(y=0, x=min_max_line[0][0])
    dir = Dir.RIGHT
    path = {}
    for turn, length in chunk(instructions, size=2):
        dir = do_turn(dir, turn)
        i = 0
        next = cur
        dir_new = dir
        while next not in walls and i <= int(length):
            cur = next
            dir = dir_new
            dir_new, next = get_next_real(cur, dir, min_max_line, min_max_row)
            i += 1
    return 1000 * (cur.y + 1) + 4 * (cur.x + 1) + get_facing_value(dir)


def tests(min_max_line, min_max_row):
    dir, p = get_next_real(Point(149, 0), Dir.RIGHT, min_max_line, min_max_row)
    assert (dir == Dir.LEFT and Point(99, 149) == p)
    dir, p = get_next_real(Point(149, 49), Dir.RIGHT, min_max_line, min_max_row)
    assert (dir == Dir.LEFT and Point(99, 100) == p)

    dir, p = get_next_real(Point(99, 50), Dir.RIGHT, min_max_line, min_max_row)
    assert (dir == Dir.UP and Point(100, 49) == p)
    dir, p = get_next_real(Point(99, 99), Dir.RIGHT, min_max_line, min_max_row)
    assert (dir == Dir.UP and Point(149, 49) == p)

    dir, p = get_next_real(Point(99, 100), Dir.RIGHT, min_max_line, min_max_row)
    assert (dir == Dir.LEFT and Point(149, 49) == p)
    dir, p = get_next_real(Point(99, 149), Dir.RIGHT, min_max_line, min_max_row)
    assert (dir == Dir.LEFT and Point(149, 0) == p)

    dir, p = get_next_real(Point(49, 150), Dir.RIGHT, min_max_line, min_max_row)
    assert (dir == Dir.UP and Point(50, 149) == p)
    dir, p = get_next_real(Point(49, 199), Dir.RIGHT, min_max_line, min_max_row)
    assert (dir == Dir.UP and Point(99, 149) == p)

    dir, p = get_next_real(Point(50, 0), Dir.LEFT, min_max_line, min_max_row)
    assert (dir == Dir.RIGHT and Point(0, 149) == p)
    dir, p = get_next_real(Point(50, 49), Dir.LEFT, min_max_line, min_max_row)
    assert (dir == Dir.RIGHT and Point(0, 100) == p)

    dir, p = get_next_real(Point(50, 50), Dir.LEFT, min_max_line, min_max_row)
    assert (dir == Dir.DOWN and Point(0, 100) == p)
    dir, p = get_next_real(Point(50, 99), Dir.LEFT, min_max_line, min_max_row)
    assert (dir == Dir.DOWN and Point(49, 100) == p)

    dir, p = get_next_real(Point(0, 100), Dir.LEFT, min_max_line, min_max_row)
    assert (dir == Dir.RIGHT and Point(50, 49) == p)
    dir, p = get_next_real(Point(0, 149), Dir.LEFT, min_max_line, min_max_row)
    assert (dir == Dir.RIGHT and Point(50, 0) == p)

    dir, p = get_next_real(Point(0, 150), Dir.LEFT, min_max_line, min_max_row)
    assert (dir == Dir.DOWN and Point(50, 0) == p)
    dir, p = get_next_real(Point(0, 199), Dir.LEFT, min_max_line, min_max_row)
    assert (dir == Dir.DOWN and Point(99, 0) == p)

    dir, p = get_next_real(Point(0, 100), Dir.UP, min_max_line, min_max_row)
    assert (dir == Dir.RIGHT and Point(50, 50) == p)
    dir, p = get_next_real(Point(49, 100), Dir.UP, min_max_line, min_max_row)
    assert (dir == Dir.RIGHT and Point(50, 99) == p)

    dir, p = get_next_real(Point(50, 0), Dir.UP, min_max_line, min_max_row)
    assert (dir == Dir.RIGHT and Point(0, 150) == p)
    dir, p = get_next_real(Point(99, 0), Dir.UP, min_max_line, min_max_row)
    assert (dir == Dir.RIGHT and Point(0, 199) == p)

    dir, p = get_next_real(Point(100, 0), Dir.UP, min_max_line, min_max_row)
    assert (dir == Dir.UP and Point(0, 199) == p)
    dir, p = get_next_real(Point(149, 0), Dir.UP, min_max_line, min_max_row)
    assert (dir == Dir.UP and Point(49, 199) == p)

    dir, p = get_next_real(Point(0, 199), Dir.DOWN, min_max_line, min_max_row)
    assert (dir == Dir.DOWN and Point(100, 0) == p)
    dir, p = get_next_real(Point(49, 199), Dir.DOWN, min_max_line, min_max_row)
    assert (dir == Dir.DOWN and Point(149, 0) == p)

    dir, p = get_next_real(Point(50, 149), Dir.DOWN, min_max_line, min_max_row)
    assert (dir == Dir.LEFT and Point(49, 150) == p)
    dir, p = get_next_real(Point(99, 149), Dir.DOWN, min_max_line, min_max_row)
    assert (dir == Dir.LEFT and Point(49, 199) == p)

    dir, p = get_next_real(Point(100, 49), Dir.DOWN, min_max_line, min_max_row)
    assert (dir == Dir.LEFT and Point(99, 50) == p)
    dir, p = get_next_real(Point(149, 49), Dir.DOWN, min_max_line, min_max_row)
    assert (dir == Dir.LEFT and Point(99, 99) == p)


def main():
    lines = input_as_str_nostrip("input_22.txt")
    walls, free, min_max_line, min_max_row, instructions = parse_input(lines)
    print("Part 1:", part_1(walls, free, min_max_line, min_max_row, instructions))
    print("Part 2:", part_2(walls, free, min_max_line, min_max_row, instructions))  # 123265 too low


if __name__ == '__main__':
    main()
