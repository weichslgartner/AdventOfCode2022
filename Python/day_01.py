import heapq
from typing import List

from aoc import input_as_str


def part_1(heap: List) -> int:
    return -heap[0]


def part_2(heap: List) -> int:
    return -sum(heapq.nsmallest(3, heap))


def to_heap(lines):
    sums = [-sum([int(x) for x in i.split("\n")]) for i in lines.split("\n\n")]
    heapq.heapify(sums)
    return sums


def main():
    in_str = input_as_str("input_01.txt").strip()
    calories_heap = to_heap(in_str)
    print("Part 1:", part_1(calories_heap))
    print("Part 2:", part_2(calories_heap))


if __name__ == '__main__':
    main()
