from aoc import get_lines, Point


def parse_input(lines):
    blocked_by = [[]]
    grid = [[]]
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[y].append(int(c))
            blocked_by[y].append(1)
        grid.append([])
        blocked_by.append([])
    return lines, blocked_by


def part_1(grid, blocked_by):
    x_max = len(grid[0])
    y_max = len(grid)
    max_point = Point(x_max, y_max)
    seen_set = set()

    sets = set()
    ranges = [(range(y_max), range(x_max), False), (list(range(y_max)), list(reversed(range(x_max))), False),
              (range(x_max), range(y_max), True), (range(x_max), list(reversed(range(y_max))), True)]
    for r0, r1, invert in ranges:
        for i in r0:
            neighbors = []
            for j in r1:
                cur = Point(i,j)
                if invert:
                    cur = Point(j,i)
                add_to_seen_and_blocked(grid, max_point, neighbors, seen_set, cur, blocked_by)
                neighbors.append(cur)

    return len(seen_set)





def add_to_seen_and_blocked(grid, max_point, neighbors, seen_set, cur, blocked_by):
    if len(neighbors) > 0:
        if all(grid[cur.y][cur.x] > grid[n.y][n.x] for n in neighbors):
            seen_set.add(cur)
        blocked_n = 0
        for n in reversed(neighbors):
            blocked_n += 1
            if grid[n.y][n.x] >= grid[cur.y][cur.x]:
                break
        blocked_by[cur.y][cur.x] *= blocked_n
    else:
        blocked_by[cur.y][cur.x] = 0
        seen_set.add(cur)


def part_2(blocked_by):
    max_tree = 0
    for line in blocked_by:
        for i in line:
            max_tree = max(i, max_tree)
    return max_tree


def main():
    lines = get_lines("input_08.txt")
    grid, blocked_by = parse_input(lines)
    print("Part 1:", part_1(grid, blocked_by)) #1662
    print("Part 2:", part_2(blocked_by)) # 537600


if __name__ == '__main__':
    main()
