from aoc import *


def parse_input(lines):
    points = []
    maxy = 0
    for line in lines:
        cur = []
        for c in chunk(extract_all_ints(line), size=2):
            cur.append(Point(int(c[0]), int(c[1])))
            maxy = max(maxy, c[1])
        points.append(cur)
    return points, maxy


def enter_sand(rocks, sands, maxy, is_part1):
    sand_p = Point(500, 0)
    while True:
        if sand_p.y > maxy:
            if is_part1:
                return False
            else:
                break
        down = Point(sand_p.x, sand_p.y + 1)
        down_left = Point(sand_p.x - 1, sand_p.y + 1)
        down_right = Point(sand_p.x + 1, sand_p.y + 1)
        if down not in rocks and down not in sands:
            sand_p = down
        elif down_left not in rocks and down_left not in sands:
            sand_p = down_left
        elif down_right not in rocks and down_right not in sands:
            sand_p = down_right
        else:
            break
    sands.add(sand_p)
    if sand_p == Point(500, 0):
        return False
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


def print_grid(rocks, sands):
    for y in range(13):
        for x in range(480, 520):
            p = Point(x, y)
            if p in rocks:
                print('#', end="")
            elif p in sands:
                print('o', end="")

            else:
                print('.', end="")
        print()


def part_1(rocks, maxy):
    sands = set()
    while enter_sand(rocks, sands, maxy, True):
        pass
    return len(sands)


def part_2(rocks, maxy):
    sands = set()
    while enter_sand(rocks, sands, maxy, False):
        pass
    return len(sands)


def main():
    lines = get_lines("input_14.txt")
    points, maxy = parse_input(lines)
    rocks = add_rocks(points)
    print("Part 1:", part_1(rocks, maxy))
    print("Part 2:", part_2(rocks, maxy))


if __name__ == '__main__':
    main()
