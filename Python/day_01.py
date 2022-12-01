import heapq

from aoc import get_lines
from pathlib import Path


def parse_input(lines):
    return lines


def part_1(lines):
    max_sum = 0
    cur_sum = 0
    for i in lines:
        if i == "":
            max_sum = max(cur_sum, max_sum)
            cur_sum = 0
        else:
            cur_sum += int(i)
    return max(cur_sum, max_sum)


def part_2(lines):
    sums = []
    heapq.heapify(sums)
    cur_sum = 0
    for i in lines:
        if i == "":
            heapq.heappush(sums,-cur_sum)
            cur_sum = 0
        else:
            cur_sum += int(i)
    return -sum([heapq.heappop(sums) for _ in range(3)])


def main():
    lines = get_lines("input_01.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
