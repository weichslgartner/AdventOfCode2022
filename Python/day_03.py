from functools import reduce
from typing import List, Iterable

from aoc import get_lines


def chunk(lines: List[str], size=3) -> List[str]:
    for i in range(0, len(lines), size):
        yield lines[i:i + size]


def calc_prio(common: str) -> int:
    if common.islower():
        return ord(common) - ord('a') + 1
    return ord(common) - ord('A') + 27


def split_line_in_half(line: str) -> (str, str):
    return line[:len(line) // 2], line[len(line) // 2:]


def find_common_char(words: Iterable[str]) -> str:
    return reduce(lambda accu, x: accu & set(x), words, set(next(words))).pop()


def part_1(lines: List[str]) -> int:
    return sum(map(lambda x: calc_prio(find_common_char(iter(x))), map(split_line_in_half, lines)))


def part_2(lines: List[str]) -> int:
    return sum(calc_prio(find_common_char(iter(c))) for c in chunk(lines))


def main():
    lines = get_lines("input_03.txt")
    print("Part 1:", part_1(lines)) # Part 1: 8176
    print("Part 2:", part_2(lines)) # Part 2: 2689


if __name__ == '__main__':
    main()
