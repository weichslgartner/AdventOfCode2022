from aoc import get_lines, input_as_str
from pathlib import Path


def parse_line(line):
    lists = []
    stack = []
    cur_list = None
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
            pass
        elif c == ']':
            if len(stack) > 0:
                stack[-1].append(cur_list)
                cur_list = stack.pop()
        else:
            cur_list.append(int(c))
    return lists


def parse_input(lines):
    for pairs in lines.split("\n\n"):
        for line in pairs.splitlines():
#
            print(parse_line((line)))
    return lines


def part_1(lines):
    pass


def part_2(lines):
    pass


def main():
    lines = input_as_str("input_13_test.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
