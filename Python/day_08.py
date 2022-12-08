from typing import List, Set

from aoc import get_lines, Point


def parse_input(lines: List[str]) -> (List[List[int]], List[List[int]]):
    return [[int(c) for c in line] for line in lines], [[1 for _ in line] for line in lines]


def generate_seen_and_blocked(blocked_by: List[List[int]], grid: List[List[int]]) -> (Set[Point], List[List[int]]):
    assert (len(grid) > 0)
    x_max = len(grid[0])
    y_max = len(grid)
    seen_set = set()
    ranges = [(range(y_max), range(x_max), False), (list(range(y_max)), list(reversed(range(x_max))), False),
              (range(x_max), range(y_max), True), (range(x_max), list(reversed(range(y_max))), True)]
    # iterate over 4 directions
    for r0, r1, invert in ranges:
        for i in r0:
            neighbors = []
            for j in r1:
                cur = to_point(i, j, invert)
                add_to_seen_and_blocked(grid, neighbors, seen_set, cur, blocked_by)
                neighbors.append(cur)
    return seen_set, blocked_by


def to_point(i: int, j: int, invert: bool) -> Point:
    if invert:
        return Point(j, i)
    return Point(i, j)


def add_to_seen_and_blocked(grid: List[List[int]], neighbors: List[Point], seen_set: Set[Point], cur: Point,
                            blocked_by: List[List[int]]):
    if len(neighbors) > 0:
        if all(grid[cur.y][cur.x] > grid[n.y][n.x] for n in neighbors):
            seen_set.add(cur)
        add_to_block(blocked_by, cur, grid, neighbors)
    else:
        # border elements
        blocked_by[cur.y][cur.x] = 0
        seen_set.add(cur)


def add_to_block(blocked_by: List[List[int]], cur: Point, grid: List[List[int]], neighbors: List[Point]):
    blocked_n = 0
    for n in reversed(neighbors):
        blocked_n += 1
        if grid[n.y][n.x] >= grid[cur.y][cur.x]:
            break
    blocked_by[cur.y][cur.x] *= blocked_n


def part_1(seen_set: Set[Point]) -> int:
    return len(seen_set)


def part_2(blocked_by: List[List[int]]) -> int:
    return max(max(line) for line in blocked_by)


def main():
    lines = get_lines("input_08.txt")
    grid, blocked_by = parse_input(lines)
    seen_set, blocked_by = generate_seen_and_blocked(blocked_by, grid)
    print("Part 1:", part_1(seen_set))  # 1662
    print("Part 2:", part_2(blocked_by))  # 537600


if __name__ == '__main__':
    main()
