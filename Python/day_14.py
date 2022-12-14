import itertools
from typing import List, Tuple, Set

from aoc import Point, chunk, extract_all_ints, get_lines

START_POINT = Point(500, 0)


def parse_input(lines: List[str]) -> Tuple[Set[Point], int]:
    points = [[Point(*c) for c in chunk(extract_all_ints(line), size=2)] for line in lines]
    maxy = max(itertools.chain.from_iterable(points), key=lambda p: p.y)
    return add_rocks(points), maxy.y


def enter_sand(rocks: Set[Point], sands: Set[Point], maxy: int, last_point: List[Point], is_part1: bool) -> bool:
    sand_p = last_point[0] if last_point[0] not in sands else START_POINT
    while True:
        if sand_p.y > maxy:
            if is_part1:
                return False
            else:
                break
        down = Point(sand_p.x, sand_p.y + 1)
        down_left = Point(sand_p.x - 1, sand_p.y + 1)
        down_right = Point(sand_p.x + 1, sand_p.y + 1)
        if is_free(down, rocks, sands):
            last_point[0] = sand_p
            sand_p = down
        elif is_free(down_left, rocks, sands):
            last_point[0] = sand_p
            sand_p = down_left
        elif is_free(down_right, rocks, sands):
            last_point[0] = sand_p
            sand_p = down_right
        else:
            break
    sands.add(sand_p)
    if sand_p == START_POINT:
        return False
    return True


def is_free(pos: Point, rocks: Set[Point], sands: Set[Point]) -> bool:
    return pos not in rocks and pos not in sands


def add_rocks(lines: List[List[Point]]) -> Set[Point]:
    rocks = set()
    for line in lines:
        for p1, p2 in zip(line, line[1:]):
            for x in range(min(p1.x, p2.x), max(p1.x, p2.x) + 1):
                rocks.add(Point(x, p1.y))
            for y in range(min(p1.y, p2.y), max(p1.y, p2.y) + 1):
                rocks.add(Point(p1.x, y))
    return rocks


def part_1(rocks: Set[Point], maxy: int) -> int:
    sands = set()
    last_point = [START_POINT]
    while enter_sand(rocks, sands, maxy, last_point, True):
        pass
    return len(sands)


def part_2(rocks: Set[Point], maxy: int) -> int:
    sands = set()
    last_point = [START_POINT]
    while enter_sand(rocks, sands, maxy, last_point, False):
        pass
    return len(sands)


def main():
    lines = get_lines("input_14.txt")
    rocks, maxy = parse_input(lines)
    print("Part 1:", part_1(rocks, maxy))
    print("Part 2:", part_2(rocks, maxy))


if __name__ == '__main__':
    main()
