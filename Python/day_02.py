from functools import reduce
from typing import List

from aoc import get_lines

points = {'X': 1, 'Y': 2, 'Z': 3}

second = {'X': 0, 'Y': 3, 'Z': 6}

win = ["A Y", "B Z", "C X"]
draw = ["A X", "B Y", "C Z"]
lose = ["A Z", "B X", "C Y"]


def convert(line):
    if second[line[-1]] == 0:
        return list(filter(lambda x: x[0] == line[0], lose))[0]
    if second[line[-1]] == 3:
        return list(filter(lambda x: x[0] == line[0], draw))[0]
    return list(filter(lambda x: x[0] == line[0], win))[0]


def part_1(lines: List[str]) -> int:
    return reduce(lambda accu, line: accu + points[line[-1]] + (line in win) * 6 + (line in draw) * 3, lines, 0)


def part_2(lines: List[str]) -> int:
    return reduce(lambda accu, line: accu + second[line[-1]] + points[convert(line)[-1]], lines, 0)


def main():
    lines = get_lines("input_02.txt")
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
