import heapq
import sys
from collections import deque, defaultdict

from aoc import get_lines, Point, get_neighbours_4, manhattan_distance
from pathlib import Path


def parse_input(lines):
    grid = [[1 for c in line] for line in lines]
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[y][x] = ord(c)
            if c == 'S':
                start = Point(x, y)
                grid[y][x] = ord('a')
            if c == 'E':
                goal = Point(x, y)
                grid[y][x] = ord('z')

    return grid, start, goal, Point(len(lines[0]), len(lines))


def part_1(grid, start, goal, maxp):
    assert (grid[goal.y][goal.x] == ord('z'))
    assert (grid[start.y][start.x] == ord('a'))

    print(start, goal)
    deq = []
    deq.append((manhattan_distance(start, goal), 0, start))
    best = sys.maxsize
    visited = set()
    while len(deq) > 0:
        # print(len(visited), len(deq))
        _, dist, cur = heapq.heappop(deq)
        if dist > best:
            continue
        # print(_,dist,cur)
        if cur == goal:
            # return dist
            best = min(best, dist)
        visited.add(cur)
        neighbors = get_neighbours_4(cur, maxp)
        for n in neighbors:
            if grid[n.y][n.x] <= grid[cur.y][cur.x] + 1 and n not in visited:
                heapq.heappush(deq, (manhattan_distance(n, goal), dist + 1, n))
    return best


def part_1(grid, start, goal, maxp) -> int:
    return a_star(grid, start, goal, maxp, True)

def part_2(grid, start, p_target, maxp) -> int:
    return a_star(grid, start, p_target, maxp,False)

def a_star(grid, start, p_target, maxp, is_part1) -> int:
    costs, f_costs, in_queue, queue = init_a_start(grid, p_target, start,is_part1)
    while len(queue) > 0:
        assert (len(queue) == len(in_queue))
        _, cur = heapq.heappop(queue)
        in_queue.remove(cur)
        if cur == p_target:
            return costs[cur]
        for n in get_neighbours_4(cur, maxp):
            if grid[n.y][n.x] > grid[cur.y][cur.x] + 1:
                continue
            t_costs = costs[cur] + 1
            if t_costs < costs[n]:
                costs[n] = t_costs
                f_costs[n] = t_costs + manhattan_distance(n, p_target)
                if n not in in_queue:
                    heapq.heappush(queue, (f_costs[n], n))
                    in_queue.add(n)


def init_a_start(grid, p_target, start, is_part_1: bool):
    costs = defaultdict(lambda: sys.maxsize)
    f_costs = defaultdict(lambda: sys.maxsize)
    in_queue = {start}
    queue = []
    costs[start] = 0
    f_costs[start] = manhattan_distance(start, p_target)
    if is_part_1:
        queue.append((manhattan_distance(start, p_target),start))
        return costs, f_costs, in_queue, queue
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == ord('a'):
                p = Point(x, y)
                in_queue.add(p)
                heapq.heappush(queue, (manhattan_distance(p, p_target), p))
                f_costs[p] = manhattan_distance(p, p_target)
                costs[p] = 0
    return costs, f_costs, in_queue, queue


def main():
    lines = get_lines("input_12.txt")
    grid, start, goal, maxp = parse_input(lines)
    print("Part 1:", part_1(grid, start, goal, maxp))
    print("Part 2:", part_2(grid, start, goal, maxp))


if __name__ == '__main__':
    main()
