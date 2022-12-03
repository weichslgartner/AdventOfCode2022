from enum import Enum
from typing import List

from aoc import get_lines


class Result(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


points = {'X': 1, 'Y': 2, 'Z': 3}

second = {'X': Result.LOSE.value, 'Y': Result.DRAW.value, 'Z': Result.WIN.value}

win = ["A Y", "B Z", "C X"]
draw = ["A X", "B Y", "C Z"]
lose = ["A Z", "B X", "C Y"]

pt2res = {Result.LOSE.value: lose, Result.DRAW.value: draw, Result.WIN.value: win}


def convert(line: str) -> str:
    return next(x for x in pt2res[second[line[-1]]] if x[0] == line[0])


def part_1(lines: List[str]) -> int:
    return sum(map(lambda line: points[line[-1]] + (line in win) * Result.WIN.value + (
            line in draw) * Result.DRAW.value, lines))


def part_2(lines: List[str]) -> int:
    return sum(map(lambda line: second[line[-1]] + points[convert(line)[-1]], lines))


def main():
    lines = get_lines("input_02.txt")
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
