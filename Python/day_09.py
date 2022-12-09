from typing import List

from aoc import get_lines, Point


def get_neighbours_8(p: Point) -> List[Point]:
    return [Point(p.x + x, p.y + y) for y in range(-1, 2) for x in range(-1, 2) if x != 0 or y != 0]


def parse_input(lines: List[str]) -> List[(str, str)]:
    return [line.split() for line in lines]


def dir_to_point(dir: str) -> Point:
    if dir == 'R':
        return Point(1, 0)
    if dir == 'L':
        return Point(-1, 0)
    if dir == 'U':
        return Point(0, 1)
    if dir == 'D':
        return Point(0, -1)


def sign(x: int) -> int:
    if x == 0:
        return 0
    if x < 0:
        return -1
    return 1


def solve(commands: List[(str, str)], length: int = 10) -> int:
    positions = {i: Point(0, 0) for i in range(length)}
    tail_set = set()
    for direct, l in commands:
        p = dir_to_point(direct)
        for _ in range(int(l)):
            positions[0] = Point(positions[0].x + p.x, positions[0].y + p.y)
            for i in range(1, length):
                if positions[i - 1] not in get_neighbours_8(positions[i]):
                    positions[i] = Point(positions[i].x + sign(positions[i - 1].x - positions[i].x),
                                         positions[i].y + sign(positions[i - 1].y - positions[i].y))
                if i == length - 1:
                    tail_set.add(positions[length - 1])
    return len(tail_set)


def part_1(commands: List[(str, str)]) -> int:
    return solve(commands, 2)


def part_2(commands: List[(str, str)]) -> int:
    return solve(commands, 10)


def main():
    lines = get_lines("input_09.txt")
    commands = parse_input(lines)
    print("Part 1:", solve(commands, 2))
    print("Part 2:", solve(commands))


if __name__ == '__main__':
    main()
