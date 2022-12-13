from enum import Enum

from aoc import get_lines, input_as_str
from pathlib import Path
from itertools import zip_longest


class Order(Enum):
    WRONG = 0
    RIGHT = 1
    CONTINUE = 2


def parse_line(line):
    lists = []
    stack = []
    cur_list = None
    number = ""
    for c in line:
        if c == '[':
            if cur_list is not None:
                if len(stack) > 0:
                    stack.append(cur_list)
                else:
                    stack.append(cur_list)
                cur_list = []
            else:
                cur_list = lists
        elif c == ',':
            if len(number) > 0:
                cur_list.append(int(number))
                number = ""
        elif c == ']':
            if len(number) > 0:
                cur_list.append(int(number))
                number = ""
            if len(stack) > 0:
                stack[-1].append(cur_list)
                cur_list = stack.pop()
        else:
            number += c
    return lists

def parse_line_eval(line):
    return eval(line)

def parse_input(lines):
    lists = []
    for pairs in lines.split("\n\n"):
        pair = []
        for line in pairs.splitlines():
            #pair.append(parse_line(line))
            pair.append(parse_line_eval(line))
        lists.append(pair)
    return lists


def compare(a, b):
    if a is None:
        return Order.RIGHT
    if b is None:
        return Order.WRONG
    if isinstance(a, list) and not isinstance(b, list):
        return compare(a, [b])
    if not isinstance(a, list) and isinstance(b, list):
        return compare([a], b)
    if isinstance(a, list) and isinstance(b, list):
        for new_a, new_b in zip_longest(a, b):
            res = compare(new_a, new_b)
            if res == Order.WRONG:
                return Order.WRONG
            if res == Order.RIGHT:
                return Order.RIGHT
    if a < b:
        return Order.RIGHT
    if a > b:
        return Order.WRONG
    return Order.CONTINUE


def part_1(pairs):
    sum = 0
    for i, pair in enumerate(pairs):
        if compare(pair[0], pair[1]) == Order.RIGHT:
            print(i + 1, "True")
            sum += (i + 1)
    print(len(pairs))
    return sum


def part_2(lines):
    pass


def main():
    lines = input_as_str("input_13.txt")

    lists = parse_input(lines)
    print("Part 1:", part_1(lists))  # 4251 too tlow too high 11325 wrong 5326
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
