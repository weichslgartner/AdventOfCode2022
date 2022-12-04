from typing import List, Callable

from aoc import get_lines, line_to_int


def parse_input(lines: List[str]) -> List[List[List[int]]]:
    return list(map(lambda line: [line_to_int(p, '-') for p in line.split(',')], lines))


def complete_overlap(p1: List[int], p2: List[int]) -> bool:
    return (p2[1] <= p1[1] and p2[0] >= p1[0]) or (p1[1] <= p2[1] and p1[0] >= p2[0])


def partial_overlap(p1: List[int], p2: List[int]) -> bool:
    if p2[0] < p1[0]:
        p1, p2 = p2, p1
    return p2[0] <= p1[1]


def solve(pairs: List[List[List[int]]], overlap: Callable[[List[int], List[int]], bool]) -> int:
    return sum(map(lambda p: overlap(*p), pairs))


def part_1(pairs: List[List[List[int]]]) -> int:
    return solve(pairs, complete_overlap)


def part_2(pairs: List[List[List[int]]]) -> int:
    return solve(pairs, partial_overlap)


def main():
    lines = get_lines("input_04.txt")
    pairs = parse_input(lines)
    print("Part 1:", part_1(pairs))  # 584
    print("Part 2:", part_2(pairs))  # 933


if __name__ == '__main__':
    main()
