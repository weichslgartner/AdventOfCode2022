from aoc import get_lines, Point, is_in_grid
from pathlib import Path


def parse_input(lines):
    blocked_by = [[]]
    grid = [[]]
    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            grid[y].append(int(c))
            blocked_by[y].append(1)
        grid.append([])
        blocked_by.append([])
    return lines, blocked_by


def part_1(grid,blocked_by):
    x_max = len(grid[0])
    y_max = len(grid)
    max_point = Point(x_max,y_max)
    seen_set = set()

    sets = set()
    ranges = [(range(y_max),range(x_max)), (range(y_max),reversed(range(x_max)),(range(x_max),range(y_max)) )]
    print_blocked(blocked_by, x_max, y_max)

    for y in range(y_max):
        neighbors = []
        for x in range(x_max):
            cur = Point(x,y)
            add_to_seen(grid, max_point, neighbors, seen_set, cur, blocked_by)
            neighbors.append(cur)

    sets |= seen_set
    seen_set = set()
    print_blocked(blocked_by, x_max, y_max)

    for y in range(y_max):
        neighbors = []
        for x in reversed(range(x_max)):
            cur = Point(x, y)
            add_to_seen(grid, max_point, neighbors, seen_set, cur, blocked_by)
            neighbors.append(cur)

    sets |= seen_set
    seen_set = set()
    print_blocked(blocked_by, x_max, y_max)

    for x in range(x_max):
        neighbors = []
        for y in reversed(range(y_max)):
            cur = Point(x, y)
            add_to_seen(grid, max_point, neighbors, seen_set, cur, blocked_by)
            neighbors.append(cur)


    sets |= seen_set
    seen_set = set()
    print(seen_set)
    for x in range(x_max):
        neighbors = []
        for y in range(y_max):
            cur = Point(x, y)
            add_to_seen(grid, max_point, neighbors, seen_set, cur, blocked_by)
            neighbors.append(cur)
    sets |= seen_set
    print_blocked(blocked_by, x_max, y_max)
    return len(sets)


def print_blocked(blocked_by, x_max, y_max):
    print()
    for y in range(y_max):
        for x in range(x_max):
            print(blocked_by[y][x], end=" ")

        print()


def print_seen_Set(grid, seen_set, x_max, y_max):
    for y in range(y_max):
        for x in range(x_max):
            if Point(x, y) in seen_set:
                print(grid[y][x], end="")
            else:
                print('N', end="")
        print()


def add_to_seen(grid, max_point, neighbors, seen_set, cur, blocked_by):
    if len(neighbors) > 0:
        if all(grid[cur.y][cur.x] > grid[n.y][n.x] for n in neighbors) :
            seen_set.add(cur)
        blocked_n = 0
        for n in reversed(neighbors):
            blocked_n += 1
            if grid[n.y][n.x] >= grid[cur.y][cur.x]  :
                break

        blocked_by[cur.y][cur.x] *= blocked_n
    else:
        blocked_by[cur.y][cur.x] =0
        seen_set.add(cur)


def part_2(blocked_by):
    max_tree = 0
    for line in blocked_by:
        for i in line:
            max_tree=max(i,max_tree)
    return max_tree



def main():
    lines = get_lines("input_08.txt")
    grid, blocked_by = parse_input(lines)
    print("Part 1:", part_1(grid,blocked_by))
    print("Part 2:", part_2(blocked_by))


if __name__ == '__main__':
    main()
