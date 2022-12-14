from typing import Tuple

from Python.day_03 import chunk
from aoc import  *


def parse_input(lines):
    points = []
    maxy = 0
    for line in lines:
        cur = []
        for c in chunk(extract_all_ints(line), size=2):
            cur.append(Point(int(c[0]),int(c[1])))
            maxy = max(maxy,c[1])
        points.append(cur)
        #points.append([[t for t in token.strip().split(',')] for token in line.split("->")])
    print(points)
    return points,maxy


def part_1(lines,maxy):
    rocks = add_rocks(lines)
    sands = set()
    cnt = 0
    while enter_sand(rocks, sands,maxy):
        cnt+=1
   # print_grid(rocks,sands)
    return len(sands)


def enter_sand(rocks, sands,maxy):
    sandP = Point(500, 0)
    while True:
        if sandP.y > maxy:
            return False
        down = Point(sandP.x, sandP.y + 1)
        down_left = Point(sandP.x - 1, sandP.y + 1)
        down_right = Point(sandP.x + 1, sandP.y + 1)
        if down not in rocks and down not in sands:
            sandP = down
        elif down_left not in rocks and down_left not in sands:
            sandP = down_left
        elif down_right not in rocks and down_right not in sands:
            sandP =down_right
        else:
            break
    sands.add(sandP)
    return True

def add_rocks(lines):
    rocks = set()
    for line in lines:
        for p1, p2 in zip(line, line[1:]):
            for x in range(min(p1.x, p2.x), max(p1.x, p2.x) + 1):
                rocks.add(Point(x, p1.y))
            for y in range(min(p1.y, p2.y), max(p1.y, p2.y) + 1):
                rocks.add(Point(p1.x, y))
    return rocks


def print_grid(rocks,sands):
    for y in range(10):
        for x in range(494, 504):
            p = Point(x, y)
            if p in rocks:
                print('#', end="")
            elif p in sands:
                print('o', end="")

            else:
                print('.', end="")
        print()


def part_2(lines):
    pass


def main():
    lines = get_lines("input_14.txt")
    points,maxy = parse_input(lines)
    print("Part 1:", part_1(points,maxy))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
