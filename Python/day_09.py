from typing import List, Tuple, Dict

from aoc import get_lines, Point


def get_neighbours_8(p: Point) -> List[Point]:
    return [Point(p.x + x, p.y + y) for y in range(-1, 2) for x in range(-1, 2) if x != 0 or y != 0]


def parse_input(lines: List[str]) -> List[Tuple[str, int]]:
    return [(e[0], int(e[1])) for e in map(lambda x: x.split(), lines)]


def dir_to_point(direction: str) -> Point:
    if direction == 'R':
        return Point(1, 0)
    if direction == 'L':
        return Point(-1, 0)
    if direction == 'U':
        return Point(0, 1)
    if direction == 'D':
        return Point(0, -1)


def sign(x: int) -> int:
    if x == 0:
        return 0
    if x < 0:
        return -1
    return 1


def solve(commands: List[Tuple[str, int]], length: int = 10) -> int:
    positions = {i: Point(0, 0) for i in range(length)}
    tail_set = set()
    for direct, steps in commands:
        direct_point = dir_to_point(direct)
        for _ in range(steps):
            positions[0] = move_head(positions[0], direct_point)
            move_body_and_tail(positions)
            tail_set.add(positions[length - 1])
    return len(tail_set)


def move_body_and_tail(positions: Dict[int, Point]):
    for i in range(1, len(positions)):
        if positions[i - 1] not in get_neighbours_8(positions[i]):
            positions[i] = Point(positions[i].x + sign(positions[i - 1].x - positions[i].x),
                                 positions[i].y + sign(positions[i - 1].y - positions[i].y))


def move_head(head: Point, direct_point: Point) -> Point:
    return Point(head.x + direct_point.x, head.y + direct_point.y)


def part_1(commands: List[Tuple[str, int]]) -> int:
    return solve(commands, 2)


def part_2(commands: List[Tuple[str, int]]) -> int:
    return solve(commands, 10)


def main():
    lines = get_lines("input_09.txt")
    commands = parse_input(lines)
    print("Part 1:", solve(commands, 2))  # 5874
    print("Part 2:", solve(commands, 10))  # 2467


if __name__ == '__main__':
    main()
