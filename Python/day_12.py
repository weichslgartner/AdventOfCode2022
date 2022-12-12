import heapq
import sys
from collections import defaultdict
from typing import List, Tuple, Dict, Set

from aoc import get_lines, Point, get_neighbours_4, manhattan_distance


def parse_input(lines: List[str]) -> Tuple[List[List[int]], Point, Point, Point]:
    grid = [[1 for _ in line] for line in lines]
    start, goal = None, None
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


def a_star(grid: List[List[int]], start: Point, goal: Point, maxp: Point, is_part1: bool) -> int:
    costs, in_queue, queue = init_a_star(grid, goal, start, is_part1)
    while len(queue) > 0:
        _, cur = heapq.heappop(queue)
        in_queue.remove(cur)
        if cur == goal:
            return costs[cur]
        for n in filter(lambda p: is_valid_neighbor(grid, cur=cur, neighbor=p), get_neighbours_4(cur, maxp)):
            t_costs = costs[cur] + 1
            if t_costs < costs[n]:
                costs[n] = t_costs
                if n not in in_queue:
                    heapq.heappush(queue, (t_costs + manhattan_distance(n, goal), n))
                    in_queue.add(n)
    return sys.maxsize


def is_valid_neighbor(grid: List[List[int]], cur: Point, neighbor: Point) -> bool:
    return grid[neighbor.y][neighbor.x] <= grid[cur.y][cur.x] + 1


def init_a_star(grid: List[List[int]], p_target: Point, start: Point, is_part_1: bool) -> \
        Tuple[Dict[Point, int], Set[Point], List[Tuple[int, Point]]]:
    costs = defaultdict(lambda: sys.maxsize)
    in_queue = {start}
    queue = []
    costs[start] = 0
    if is_part_1:
        queue.append((manhattan_distance(start, p_target), start))
        return costs, in_queue, queue
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == ord('a'):
                p = Point(x, y)
                in_queue.add(p)
                heapq.heappush(queue, (manhattan_distance(p, p_target), p))
                costs[p] = 0
    return costs, in_queue, queue


def part_1(grid: List[List[int]], start: Point, goal: Point, maxp: Point) -> int:
    return a_star(grid, start, goal, maxp, True)


def part_2(grid: List[List[int]], start: Point, goal: Point, maxp: Point) -> int:
    return a_star(grid, start, goal, maxp, False)


def main():
    lines = get_lines("input_12.txt")
    grid, start, goal, maxp = parse_input(lines)
    print("Part 1:", part_1(grid, start, goal, maxp))
    print("Part 2:", part_2(grid, start, goal, maxp))


if __name__ == '__main__':
    main()
