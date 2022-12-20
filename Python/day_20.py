from typing import List, Tuple

from aoc import get_lines

decryption_key = 811589153


def parse_input(lines: List[str]) -> List:
    return list(enumerate(map(int, lines)))


def solve(lines: List[Tuple[int, int]], rounds: int) -> int:
    length = len(lines)
    elements = lines.copy()
    for _ in range(rounds):
        for n in elements:
            old_index = lines.index(n)
            if n[1] == 0:
                continue
            new_index = (old_index + n[1]) % (length - 1)
            lines.insert(new_index, lines.pop(old_index))
    idx = lines.index(list(filter(lambda x: x[1] == 0, lines)).pop())
    return sum(map(lambda x: x[1], (lines[(idx + grove) % length] for grove in [1000, 2000, 3000])))


def part_1(lines: List[Tuple[int, int]]) -> int:
    return solve(lines, 1)


def part_2(lines: List[Tuple[int, int]]) -> int:
    lines = list(map(lambda x: (x[0], x[1] * decryption_key), lines))
    return solve(lines, 10)


def main():
    lines = get_lines("input_20.txt")  # too low 6711
    lines = parse_input(lines)
    print("Part 1:", part_1(lines.copy()))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
