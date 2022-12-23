import sys
from collections import defaultdict
from enum import Enum
from typing import List

from aoc import get_lines, Point


class Dir(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3


def dir2points(p: Point, d: Dir):
    if d == Dir.NORTH:
        return [Point(x=p.x + i, y=p.y - 1) for i in range(-1, 2)]
    if d == Dir.SOUTH:
        return [Point(x=p.x + i, y=p.y + 1) for i in range(-1, 2)]
    if d == Dir.WEST:
        return [Point(x=p.x - 1, y=p.y + i) for i in range(-1, 2)]
    if d == Dir.EAST:
        return [Point(x=p.x + 1, y=p.y + i) for i in range(-1, 2)]


def get_neighbours_8(p: Point) -> List[Point]:
    return [Point(p.x + x, p.y + y) for y in range(-1, 2) for x in range(-1, 2) if x != 0 or y != 0]


def parse_input(lines):
    elves = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                elves.add(Point(x, y))
    return elves


def solve(elves, rounds=10):
    dix = 0
    moves = {}
    move_cnt = defaultdict(int)
    new_elves = set()
    for i in range(rounds):
        # step 1
        move_cnt.clear()
        moves.clear()
        for elf in elves:
            if any((n in elves for n in get_neighbours_8(elf))):
                for d in range(len(Dir)):
                    d = Dir((d + dix) % len(Dir))
                    neighbors = dir2points(p=elf, d=d)
                    if all((n not in elves for n in neighbors)):
                        moves[elf] = neighbors[1]
                        move_cnt[neighbors[1]] += 1
                        break
        if len(moves) == 0:
            return i + 1
        # step 2
        new_elves.clear()
        for elf in elves:
            if elf in moves and move_cnt[moves[elf]] == 1:
                new_elves.add(moves[elf])
            else:
                new_elves.add(elf)
        elves, new_elves = new_elves, elves
        # step 3
        dix += 1
    return cnt_empty_space(elves)


def cnt_empty_space(elves):
    minx = min(elves, key=lambda p: p.x).x
    maxx = max(elves, key=lambda p: p.x).x
    miny = min(elves, key=lambda p: p.y).y
    maxy = max(elves, key=lambda p: p.y).y
    cnt = 0
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if Point(x, y) not in elves:
                cnt += 1
    return cnt


def print_gird(elves):
    for y in range(-5, 15):
        for x in range(-5, 15):
            if Point(x, y) in elves:
                print("#", end="")
            else:
                print('.', end="")
        print("")
    print()

def part_1(elves):
    return solve(elves, rounds=10)

def part_2(elves):
    return solve(elves, rounds=sys.maxsize)


def main():
    lines = get_lines("input_23.txt")
    elves = parse_input(lines)
    print("Part 1:", part_1(elves.copy()))
    print("Part 2:", part_2(elves))


if __name__ == '__main__':
    main()
