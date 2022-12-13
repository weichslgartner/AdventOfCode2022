from enum import Enum
from functools import cmp_to_key, reduce
from typing import Union, List

from aoc import input_as_str
from itertools import zip_longest, chain


class Order(Enum):
    WRONG = -1
    RIGHT = 1
    CONTINUE = 0


def parse_line(line: str) -> List[List]:
    lists = []
    stack = []
    cur_list = None
    number = ""
    for c in line:
        if c == '[':
            if cur_list is not None:
                stack.append(cur_list)
                cur_list = []
            else:
                cur_list = lists
        elif c == ',':
            number = maybe_append_number(cur_list, number)
        elif c == ']':
            number = maybe_append_number(cur_list, number)
            if len(stack) > 0:
                stack[-1].append(cur_list)
                cur_list = stack.pop()
        else:
            number += c
    return lists


def maybe_append_number(cur_list: List, number: str) -> str:
    if len(number) > 0:
        cur_list.append(int(number))
    return ""


def parse_input(lines: str) -> List:
    return [[parse_line(line) for line in pairs.splitlines()] for pairs in lines.split("\n\n")]


def compare(a: Union[int, List], b: Union[int, List]) -> int:
    if a is None:
        return Order.RIGHT.value
    if b is None:
        return Order.WRONG.value
    if isinstance(a, list) and not isinstance(b, list):
        return compare(a, [b])
    if not isinstance(a, list) and isinstance(b, list):
        return compare([a], b)
    if isinstance(a, list) and isinstance(b, list):
        for new_a, new_b in zip_longest(a, b):
            res = compare(new_a, new_b)
            if res in [Order.WRONG.value, Order.RIGHT.value]:
                return res
        return Order.CONTINUE.value
    if a < b:
        return Order.RIGHT.value
    if a > b:
        return Order.WRONG.value
    return Order.CONTINUE.value


def part_1(pairs: List) -> int:
    return sum(map(lambda x: x[0],
                   filter(lambda x: x[1] == Order.RIGHT.value,
                          map(lambda x: (x[0], compare(*x[1])),
                              enumerate(pairs, start=1)))))


def part_2(pairs: List, divider_packets: List) -> int:
    return reduce(lambda accu, x: accu * x[0],
                  filter(lambda x: x[1] in divider_packets,
                         enumerate(
                             sorted(list(chain.from_iterable(pairs)) + divider_packets,
                                    key=cmp_to_key(compare), reverse=True), start=1)),
                  1)


def main():
    lines = input_as_str("input_13.txt")
    pairs = parse_input(lines)
    print("Part 1:", part_1(pairs))
    print("Part 2:", part_2(pairs, divider_packets=[[[2]], [[6]]]))


if __name__ == '__main__':
    main()
