import re
from enum import Enum, StrEnum

from aoc import input_as_str_nostrip, Point, chunk


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
    grid, instructions = lines.split('\n\n')
    walls = set()
    free = set()
    max_x = len(grid[0])
    max_y = len(grid)
    min_max_line = {}
    min_max_row = {}
    for y, line in enumerate(grid.splitlines()):
        for x, c in enumerate(line):
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
        return Point(x_new, p.y)
    if dir == Dir.DOWN:
        y_new = p.y + 1
        if y_new > min_max_row[p.x][1]:
            y_new = min_max_row[p.x][0]
        return Point(p.x, y_new)
    if dir == Dir.LEFT:
        x_new = p.x - 1
        if x_new < min_max_line[p.y][0]:
            x_new = min_max_line[p.y][1]
        return Point(x_new, p.y)
    if dir == Dir.UP:
        y_new = p.y - 1
        if y_new < min_max_row[p.x][0]:
            y_new = min_max_row[p.x][1]
        return Point(p.x, y_new)


def part_1(walls, free, min_max_line, min_max_row, instructions):
    #print(min_max_line)
    #print(min_max_row)
    cur = Point(y=0, x=min_max_line[0][0])
    dir = Dir.RIGHT
    path = {}
    #print_grid(free, min_max_line, min_max_row, path, walls)
    for turn, length in chunk(instructions, size=2):
        dir = do_turn(dir, turn)
        #print(turn, length)
        #print(cur, dir)
        i = 0
        next = cur
        path[cur] = dir.value
        while next not in walls and i <= int(length):
            cur = next
            path[cur] = dir.value
            next = get_next(cur, dir, min_max_line, min_max_row)
            i += 1
        #print_grid(free, min_max_line, min_max_row, path, walls)
    print("finished", cur, dir)
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
    pass


def main():
    lines = input_as_str_nostrip("input_22.txt")
    walls, free, min_max_line, min_max_row, instructions = parse_input(lines)
    print("Part 1:", part_1(walls, free, min_max_line, min_max_row, instructions))
    print("Part 2:", part_2(walls, free, min_max_line, min_max_row, instructions))


if __name__ == '__main__':
    main()
