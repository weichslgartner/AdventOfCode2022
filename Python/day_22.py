import re
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Set, Dict, List, Callable

from aoc import input_as_str_nostrip, Point, chunk


class Dir(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


@dataclass
class Board:
    walls: Set[Point]
    min_max_line: Dict[int, List[int]]
    min_max_row: Dict[int, List[int]]
    width: int
    height: int
    side_sz: int


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


def parse_input(lines: str) -> Tuple[Board, List[str]]:
    width = 0
    height = 0
    grid, instructions = lines.split('\n\n')
    walls = set()
    min_max_line = {}
    min_max_row = {}
    for y, line in enumerate(grid.splitlines()):
        height = max(y, height)
        for x, c in enumerate(line):
            width = max(x, width)
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
    width += 1
    height += 1
    min_side = min(min_max_line.values(), key=lambda v: v[1] - v[0])
    cube_side_size = min_side[1] - min_side[0] + 1
    return Board(walls=walls, min_max_line=min_max_line, min_max_row=min_max_row, width=width, height=height,
                 side_sz=cube_side_size), instructions


def add_to_min_max(min_max_line: Dict[int, List[int]], entry: int, index: int):
    if index not in min_max_line:
        min_max_line[index] = [entry, entry]
    else:
        min_max_line[index][1] = entry


def get_next_wrap(p: Point, direction: Dir, board: Board) -> Tuple[Dir, Point]:
    if direction == Dir.RIGHT:
        x_new = p.x + 1
        if x_new > board.min_max_line[p.y][1]:
            x_new = board.min_max_line[p.y][0]
        return direction, Point(x_new, p.y)
    if direction == Dir.DOWN:
        y_new = p.y + 1
        if y_new > board.min_max_row[p.x][1]:
            y_new = board.min_max_row[p.x][0]
        return direction, Point(p.x, y_new)
    if direction == Dir.LEFT:
        x_new = p.x - 1
        if x_new < board.min_max_line[p.y][0]:
            x_new = board.min_max_line[p.y][1]
        return direction, Point(x_new, p.y)
    if direction == Dir.UP:
        y_new = p.y - 1
        if y_new < board.min_max_row[p.x][0]:
            y_new = board.min_max_row[p.x][1]
        return direction, Point(p.x, y_new)


def get_next_cube(p: Point, direction: Dir, board: Board) -> Tuple[Dir, Point]:
    if direction == Dir.RIGHT:
        x_new = p.x + 1
        if x_new > board.min_max_line[p.y][1]:
            if p.y < board.side_sz:
                return direction.LEFT, Point(x=2 * board.side_sz - 1, y=(3 * board.side_sz - 1) - p.y)
            elif p.y < 2 * board.side_sz:
                direction = direction.UP
                return direction, Point(x=2 * board.side_sz + (p.y - board.side_sz), y=board.side_sz - 1)
            elif p.y < 3 * board.side_sz:
                direction = direction.LEFT
                return direction, Point(x=3 * board.side_sz - 1, y=(3 * board.side_sz - 1) - p.y)
            elif p.y < 4 * board.side_sz:
                direction = direction.UP
                return direction, Point(x=board.side_sz + p.y - (3 * board.side_sz), y=(3 * board.side_sz - 1))
            else:
                print("error")
        return direction, Point(x_new, p.y)
    if direction == Dir.DOWN:
        y_new = p.y + 1
        if y_new > board.min_max_row[p.x][1]:
            if p.x < board.side_sz:
                return direction.DOWN, Point(x=2 * board.side_sz + p.x, y=0)
            elif p.x < 2 * board.side_sz:
                return direction.LEFT, Point(x=board.side_sz - 1, y=3 * board.side_sz + p.x - board.side_sz)
            elif p.x < 3 * board.side_sz:
                return direction.LEFT, Point(x=2 * board.side_sz - 1, y=board.side_sz + p.x - 2 * board.side_sz)
            else:
                print("error")
        return direction, Point(p.x, y_new)
    if direction == Dir.LEFT:
        x_new = p.x - 1
        if x_new < board.min_max_line[p.y][0]:
            if p.y < board.side_sz:
                return direction.RIGHT, Point(x=0, y=(3 * board.side_sz - 1) - p.y)
            elif p.y < 2 * board.side_sz:
                direction = direction.DOWN
                return direction, Point(x=p.y - board.side_sz, y=2 * board.side_sz)
            elif p.y < 3 * board.side_sz:
                direction = direction.RIGHT
                return direction, Point(x=board.side_sz, y=(3 * board.side_sz - 1) - p.y)
            elif p.y < 4 * board.side_sz:
                direction = direction.DOWN
                return direction, Point(x=board.side_sz + p.y - (3 * board.side_sz), y=0)
            else:
                print("error")
        return direction, Point(x_new, p.y)
    if direction == Dir.UP:
        y_new = p.y - 1
        if y_new < board.min_max_row[p.x][0]:
            if p.x < board.side_sz:
                return direction.RIGHT, Point(x=board.side_sz, y=board.side_sz + p.x)
            elif p.x < 2 * board.side_sz:
                return direction.RIGHT, Point(x=0, y=3 * board.side_sz + p.x - board.side_sz)
            elif p.x < 3 * board.side_sz:
                return direction.UP, Point(x=p.x - 2 * board.side_sz, y=4 * board.side_sz - 1)
            else:
                print("error")
        return direction, Point(p.x, y_new)


def solve(board: Board, instructions: List[str], next_fun: Callable) -> int:
    cur = Point(y=0, x=board.min_max_line[0][0])
    direction = Dir.RIGHT
    for turn, length in chunk(instructions, size=2):
        direction = do_turn(direction, turn)
        cur, direction = do_move(cur, direction, int(length), board, next_fun)
    return 1000 * (cur.y + 1) + 4 * (cur.x + 1) + direction.value


def do_move(cur: Point, direction: Dir, length: int, board: Board, next_fun: Callable) -> Tuple[Point, Dir]:
    next_pos = cur
    next_dir = direction
    for _ in range(length + 1):
        cur = next_pos
        direction = next_dir
        next_dir, next_pos = next_fun(cur, direction, board)
        if next_pos in board.walls:
            break
    return cur, direction


def part_1(board: Board, instructions: List[str]) -> int:
    return solve(board, instructions, get_next_wrap)


def part_2(board: Board, instructions: List[str]) -> int:
    return solve(board, instructions, get_next_cube)


def tests(board: Board):
    direction, p = get_next_cube(Point(149, 0), Dir.RIGHT, board)
    assert (direction == Dir.LEFT and Point(99, 149) == p)
    direction, p = get_next_cube(Point(149, 49), Dir.RIGHT, board)
    assert (direction == Dir.LEFT and Point(99, 100) == p)

    direction, p = get_next_cube(Point(99, 50), Dir.RIGHT, board)
    assert (direction == Dir.UP and Point(100, 49) == p)
    direction, p = get_next_cube(Point(99, 99), Dir.RIGHT, board)
    assert (direction == Dir.UP and Point(149, 49) == p)

    direction, p = get_next_cube(Point(99, 100), Dir.RIGHT, board)
    assert (direction == Dir.LEFT and Point(149, 49) == p)
    direction, p = get_next_cube(Point(99, 149), Dir.RIGHT, board)
    assert (direction == Dir.LEFT and Point(149, 0) == p)

    direction, p = get_next_cube(Point(49, 150), Dir.RIGHT, board)
    assert (direction == Dir.UP and Point(50, 149) == p)
    direction, p = get_next_cube(Point(49, 199), Dir.RIGHT, board)
    assert (direction == Dir.UP and Point(99, 149) == p)

    direction, p = get_next_cube(Point(50, 0), Dir.LEFT, board)
    assert (direction == Dir.RIGHT and Point(0, 149) == p)
    direction, p = get_next_cube(Point(50, 49), Dir.LEFT, board)
    assert (direction == Dir.RIGHT and Point(0, 100) == p)

    direction, p = get_next_cube(Point(50, 50), Dir.LEFT, board)
    assert (direction == Dir.DOWN and Point(0, 100) == p)
    direction, p = get_next_cube(Point(50, 99), Dir.LEFT, board)
    assert (direction == Dir.DOWN and Point(49, 100) == p)

    direction, p = get_next_cube(Point(0, 100), Dir.LEFT, board)
    assert (direction == Dir.RIGHT and Point(50, 49) == p)
    direction, p = get_next_cube(Point(0, 149), Dir.LEFT, board)
    assert (direction == Dir.RIGHT and Point(50, 0) == p)

    direction, p = get_next_cube(Point(0, 150), Dir.LEFT, board)
    assert (direction == Dir.DOWN and Point(50, 0) == p)
    direction, p = get_next_cube(Point(0, 199), Dir.LEFT, board)
    assert (direction == Dir.DOWN and Point(99, 0) == p)

    direction, p = get_next_cube(Point(0, 100), Dir.UP, board)
    assert (direction == Dir.RIGHT and Point(50, 50) == p)
    direction, p = get_next_cube(Point(49, 100), Dir.UP, board)
    assert (direction == Dir.RIGHT and Point(50, 99) == p)

    direction, p = get_next_cube(Point(50, 0), Dir.UP, board)
    assert (direction == Dir.RIGHT and Point(0, 150) == p)
    direction, p = get_next_cube(Point(99, 0), Dir.UP, board)
    assert (direction == Dir.RIGHT and Point(0, 199) == p)

    direction, p = get_next_cube(Point(100, 0), Dir.UP, board)
    assert (direction == Dir.UP and Point(0, 199) == p)
    direction, p = get_next_cube(Point(149, 0), Dir.UP, board)
    assert (direction == Dir.UP and Point(49, 199) == p)

    direction, p = get_next_cube(Point(0, 199), Dir.DOWN, board)
    assert (direction == Dir.DOWN and Point(100, 0) == p)
    direction, p = get_next_cube(Point(49, 199), Dir.DOWN, board)
    assert (direction == Dir.DOWN and Point(149, 0) == p)

    direction, p = get_next_cube(Point(50, 149), Dir.DOWN, board)
    assert (direction == Dir.LEFT and Point(49, 150) == p)
    direction, p = get_next_cube(Point(99, 149), Dir.DOWN, board)
    assert (direction == Dir.LEFT and Point(49, 199) == p)

    direction, p = get_next_cube(Point(100, 49), Dir.DOWN, board)
    assert (direction == Dir.LEFT and Point(99, 50) == p)
    direction, p = get_next_cube(Point(149, 49), Dir.DOWN, board)
    assert (direction == Dir.LEFT and Point(99, 99) == p)


def main():
    lines = input_as_str_nostrip("input_22.txt")
    board, instructions = parse_input(lines)
    tests(board)
    print("Part 1:", part_1(board, instructions))  # 197160
    print("Part 2:", part_2(board, instructions))  # 145065


if __name__ == '__main__':
    main()
