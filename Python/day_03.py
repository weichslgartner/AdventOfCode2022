from functools import reduce
from typing import List

from aoc import get_lines

test = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def chunk(lines: List[str], size=3) -> List[str]:
    for i in range(0, len(lines), size):
        yield lines[i:i + size]


def calc_prio(common: str) -> int:
    if common.islower():
        return ord(common) - ord('a') + 1
    return ord(common) - ord('A') + 27


def split_line_in_half(line: str) -> (str, str):
    return line[:len(line) // 2], line[len(line) // 2:]


def part_1(lines: List[str]) -> int:
    return sum(map(lambda x: calc_prio((set(x[0]) & set(x[1])).pop()), map(split_line_in_half, lines)))


def part_2(lines: List[str]) -> int:
    return sum(calc_prio(reduce(lambda accu, x: accu & set(x) if len(accu) > 0 else set(x), c, set()).pop()) for c in
               chunk(lines))


def main():
    lines = get_lines("input_03.txt")
    assert (part_1(test.splitlines()) == 157)
    assert (part_2(test.splitlines()) == 70)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
