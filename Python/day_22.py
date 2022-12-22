import re
import sys
from enum import Enum
from typing import Tuple, Set, Dict, List, Callable

from aoc import input_as_str_nostrip, Point, chunk

WIDTH = 0
HEIGHT = 0
CUBE_SIDE_SIZE = sys.maxsize


class Dir(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def do_turn(cur_dir: Dir, turn: str) -> Dir:
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


def parse_input(lines: str) -> Tuple[Set[Point], Dict[int, List[int]], Dict[int, List[int]], List[str]]:
    global WIDTH, HEIGHT, CUBE_SIDE_SIZE
    grid, instructions = lines.split('\n\n')
    walls = set()
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
    instructions = re.split(r'(\d+)', instructions.strip())
    instructions.pop()
    WIDTH += 1
    HEIGHT += 1
    min_side = min(min_max_line.values(), key=lambda v: v[1] - v[0])
    CUBE_SIDE_SIZE = min_side[1] - min_side[0] + 1
    return walls, min_max_line, min_max_row, instructions


def add_to_min_max(min_max_line: Dict[int, List[int]], entry: int, index: int):
    if index not in min_max_line:
        min_max_line[index] = [entry, entry]
    else:
        min_max_line[index][1] = entry


def get_next_wrap(p: Point, direction: Dir, min_max_line: Dict[int, List[int]],
                  min_max_row: Dict[int, List[int]]) -> Tuple[Dir, Point]:
    if direction == Dir.RIGHT:
        x_new = p.x + 1
        if x_new > min_max_line[p.y][1]:
            x_new = min_max_line[p.y][0]
        return direction, Point(x_new, p.y)
    if direction == Dir.DOWN:
        y_new = p.y + 1
        if y_new > min_max_row[p.x][1]:
            y_new = min_max_row[p.x][0]
        return direction, Point(p.x, y_new)
    if direction == Dir.LEFT:
        x_new = p.x - 1
        if x_new < min_max_line[p.y][0]:
            x_new = min_max_line[p.y][1]
        return direction, Point(x_new, p.y)
    if direction == Dir.UP:
        y_new = p.y - 1
        if y_new < min_max_row[p.x][0]:
            y_new = min_max_row[p.x][1]
        return direction, Point(p.x, y_new)


def get_next_cube(p: Point, direction: Dir, min_max_line: Dict[int, List[int]],
                  min_max_row: Dict[int, List[int]]) -> Tuple[Dir, Point]:
    if direction == Dir.RIGHT:
        x_new = p.x + 1
        if x_new > min_max_line[p.y][1]:
            if p.y < CUBE_SIDE_SIZE:
                return direction.LEFT, Point(x=2*CUBE_SIDE_SIZE-1, y=(3 * CUBE_SIDE_SIZE - 1) - p.y)
            elif p.y < 2 * CUBE_SIDE_SIZE:
                direction = direction.UP
                return direction, Point(x=2 * CUBE_SIDE_SIZE + (p.y - CUBE_SIDE_SIZE), y=CUBE_SIDE_SIZE - 1)
            elif p.y < 3 * CUBE_SIDE_SIZE:
                direction = direction.LEFT
                return direction, Point(x=3 * CUBE_SIDE_SIZE - 1, y=(3 * CUBE_SIDE_SIZE - 1) - p.y)
            elif p.y < 4 * CUBE_SIDE_SIZE:
                direction = direction.UP
                return direction, Point(x=CUBE_SIDE_SIZE + p.y - (3 * CUBE_SIDE_SIZE), y=(3 * CUBE_SIDE_SIZE - 1))
            else:
                print("error")
        return direction, Point(x_new, p.y)
    if direction == Dir.DOWN:
        y_new = p.y + 1
        if y_new > min_max_row[p.x][1]:
            if p.x < CUBE_SIDE_SIZE:
                return direction.DOWN, Point(x=2 * CUBE_SIDE_SIZE + p.x, y=0)
            elif p.x < 2 * CUBE_SIDE_SIZE:
                return direction.LEFT, Point(x=CUBE_SIDE_SIZE - 1, y=3 * CUBE_SIDE_SIZE + p.x - CUBE_SIDE_SIZE)
            elif p.x < 3 * CUBE_SIDE_SIZE:
                return direction.LEFT, Point(x=2 * CUBE_SIDE_SIZE - 1, y=CUBE_SIDE_SIZE + p.x - 2 * CUBE_SIDE_SIZE)
            else:
                print("error")
        return direction, Point(p.x, y_new)
    if direction == Dir.LEFT:
        x_new = p.x - 1
        if x_new < min_max_line[p.y][0]:
            if p.y < CUBE_SIDE_SIZE:
                return direction.RIGHT, Point(x=0, y=(3 * CUBE_SIDE_SIZE - 1) - p.y)
            elif p.y < 2 * CUBE_SIDE_SIZE:
                direction = direction.DOWN
                return direction, Point(x=p.y - CUBE_SIDE_SIZE, y=2 * CUBE_SIDE_SIZE)
            elif p.y < 3 * CUBE_SIDE_SIZE:
                direction = direction.RIGHT
                return direction, Point(x=CUBE_SIDE_SIZE, y=(3 * CUBE_SIDE_SIZE - 1) - p.y)
            elif p.y < 4 * CUBE_SIDE_SIZE:
                direction = direction.DOWN
                return direction, Point(x=CUBE_SIDE_SIZE + p.y - (3 * CUBE_SIDE_SIZE), y=0)
            else:
                print("error")
        return direction, Point(x_new, p.y)
    if direction == Dir.UP:
        y_new = p.y - 1
        if y_new < min_max_row[p.x][0]:
            if p.x < CUBE_SIDE_SIZE:
                return direction.RIGHT, Point(x=CUBE_SIDE_SIZE, y=CUBE_SIDE_SIZE + p.x)
            elif p.x < 2 * CUBE_SIDE_SIZE:
                return direction.RIGHT, Point(x=0, y=3 * CUBE_SIDE_SIZE + p.x - CUBE_SIDE_SIZE)
            elif p.x < 3 * CUBE_SIDE_SIZE:
                return direction.UP, Point(x=p.x - 2 * CUBE_SIDE_SIZE, y=4 * CUBE_SIDE_SIZE - 1)
            else:
                print("error")
        return direction, Point(p.x, y_new)


def solve(walls: Set[Point], min_max_line: Dict[int, List[int]], min_max_row: Dict[int, List[int]],
          instructions: List[str], next_fun: Callable) -> int:
    cur = Point(y=0, x=min_max_line[0][0])
    direction = Dir.RIGHT
    for turn, length in chunk(instructions, size=2):
        direction = do_turn(direction, turn)
        i = 0
        next_pos = cur
        dir_new = direction
        while next_pos not in walls and i <= int(length):
            cur = next_pos
            direction = dir_new
            dir_new, next_pos = next_fun(cur, direction, min_max_line, min_max_row)
            i += 1
    return 1000 * (cur.y + 1) + 4 * (cur.x + 1) + direction.value


def part_1(walls: Set[Point], min_max_line: Dict[int, List[int]], min_max_row: Dict[int, List[int]],
           instructions: List[str]) -> int:
    return solve(walls, min_max_line, min_max_row, instructions, get_next_wrap)


def part_2(walls: Set[Point], min_max_line: Dict[int, List[int]], min_max_row: Dict[int, List[int]],
           instructions: List[str]) -> int:
    return solve(walls, min_max_line, min_max_row, instructions, get_next_cube)


def tests(min_max_line: Dict[int, List[int]], min_max_row: Dict[int, List[int]]):
    direction, p = get_next_cube(Point(149, 0), Dir.RIGHT, min_max_line, min_max_row)
    assert (direction == Dir.LEFT and Point(99, 149) == p)
    direction, p = get_next_cube(Point(149, 49), Dir.RIGHT, min_max_line, min_max_row)
    assert (direction == Dir.LEFT and Point(99, 100) == p)

    direction, p = get_next_cube(Point(99, 50), Dir.RIGHT, min_max_line, min_max_row)
    assert (direction == Dir.UP and Point(100, 49) == p)
    direction, p = get_next_cube(Point(99, 99), Dir.RIGHT, min_max_line, min_max_row)
    assert (direction == Dir.UP and Point(149, 49) == p)

    direction, p = get_next_cube(Point(99, 100), Dir.RIGHT, min_max_line, min_max_row)
    assert (direction == Dir.LEFT and Point(149, 49) == p)
    direction, p = get_next_cube(Point(99, 149), Dir.RIGHT, min_max_line, min_max_row)
    assert (direction == Dir.LEFT and Point(149, 0) == p)

    direction, p = get_next_cube(Point(49, 150), Dir.RIGHT, min_max_line, min_max_row)
    assert (direction == Dir.UP and Point(50, 149) == p)
    direction, p = get_next_cube(Point(49, 199), Dir.RIGHT, min_max_line, min_max_row)
    assert (direction == Dir.UP and Point(99, 149) == p)

    direction, p = get_next_cube(Point(50, 0), Dir.LEFT, min_max_line, min_max_row)
    assert (direction == Dir.RIGHT and Point(0, 149) == p)
    direction, p = get_next_cube(Point(50, 49), Dir.LEFT, min_max_line, min_max_row)
    assert (direction == Dir.RIGHT and Point(0, 100) == p)

    direction, p = get_next_cube(Point(50, 50), Dir.LEFT, min_max_line, min_max_row)
    assert (direction == Dir.DOWN and Point(0, 100) == p)
    direction, p = get_next_cube(Point(50, 99), Dir.LEFT, min_max_line, min_max_row)
    assert (direction == Dir.DOWN and Point(49, 100) == p)

    direction, p = get_next_cube(Point(0, 100), Dir.LEFT, min_max_line, min_max_row)
    assert (direction == Dir.RIGHT and Point(50, 49) == p)
    direction, p = get_next_cube(Point(0, 149), Dir.LEFT, min_max_line, min_max_row)
    assert (direction == Dir.RIGHT and Point(50, 0) == p)

    direction, p = get_next_cube(Point(0, 150), Dir.LEFT, min_max_line, min_max_row)
    assert (direction == Dir.DOWN and Point(50, 0) == p)
    direction, p = get_next_cube(Point(0, 199), Dir.LEFT, min_max_line, min_max_row)
    assert (direction == Dir.DOWN and Point(99, 0) == p)

    direction, p = get_next_cube(Point(0, 100), Dir.UP, min_max_line, min_max_row)
    assert (direction == Dir.RIGHT and Point(50, 50) == p)
    direction, p = get_next_cube(Point(49, 100), Dir.UP, min_max_line, min_max_row)
    assert (direction == Dir.RIGHT and Point(50, 99) == p)

    direction, p = get_next_cube(Point(50, 0), Dir.UP, min_max_line, min_max_row)
    assert (direction == Dir.RIGHT and Point(0, 150) == p)
    direction, p = get_next_cube(Point(99, 0), Dir.UP, min_max_line, min_max_row)
    assert (direction == Dir.RIGHT and Point(0, 199) == p)

    direction, p = get_next_cube(Point(100, 0), Dir.UP, min_max_line, min_max_row)
    assert (direction == Dir.UP and Point(0, 199) == p)
    direction, p = get_next_cube(Point(149, 0), Dir.UP, min_max_line, min_max_row)
    assert (direction == Dir.UP and Point(49, 199) == p)

    direction, p = get_next_cube(Point(0, 199), Dir.DOWN, min_max_line, min_max_row)
    assert (direction == Dir.DOWN and Point(100, 0) == p)
    direction, p = get_next_cube(Point(49, 199), Dir.DOWN, min_max_line, min_max_row)
    assert (direction == Dir.DOWN and Point(149, 0) == p)

    direction, p = get_next_cube(Point(50, 149), Dir.DOWN, min_max_line, min_max_row)
    assert (direction == Dir.LEFT and Point(49, 150) == p)
    direction, p = get_next_cube(Point(99, 149), Dir.DOWN, min_max_line, min_max_row)
    assert (direction == Dir.LEFT and Point(49, 199) == p)

    direction, p = get_next_cube(Point(100, 49), Dir.DOWN, min_max_line, min_max_row)
    assert (direction == Dir.LEFT and Point(99, 50) == p)
    direction, p = get_next_cube(Point(149, 49), Dir.DOWN, min_max_line, min_max_row)
    assert (direction == Dir.LEFT and Point(99, 99) == p)


def main():
    lines = input_as_str_nostrip("input_22.txt")
    walls, min_max_line, min_max_row, instructions = parse_input(lines)
    tests(min_max_line, min_max_row)
    print("Part 1:", part_1(walls, min_max_line, min_max_row, instructions))  # 197160
    print("Part 2:", part_2(walls, min_max_line, min_max_row, instructions))  # 145065


if __name__ == '__main__':
    main()
