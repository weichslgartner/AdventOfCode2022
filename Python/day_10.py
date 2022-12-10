from typing import List

from aoc import get_lines

m_points = [20, 60, 100, 140, 180, 220]


def part_1(lines: List[str]) -> int:
    cycl_cnt = 1
    signal_strength = 0
    register = 1
    pos = 0
    for line in lines:
        tokenz = line.split()
        pos = print_pixel(pos, register)
        if tokenz[0] == "noop":
            cycl_cnt += 1
        if tokenz[0] == "addx":
            pos = print_pixel(pos, register)
            signal_strength = increase_signal_strength(cycl_cnt + 1, register, signal_strength)
            cycl_cnt += 2
            register += int(tokenz[1])
        signal_strength = increase_signal_strength(cycl_cnt, register, signal_strength)
    return signal_strength


def increase_signal_strength(cycl_cnt: int, register: int, signal_strength: int) -> int:
    if cycl_cnt in m_points:
        signal_strength += cycl_cnt * register
    return signal_strength


def print_pixel(pos: int, register: int):
    if pos in range(register - 1, register + 2):
        print("#", end="")
    else:
        print('.', end="")
    if pos == 39:
        print()
        return 0
    return pos + 1


def main():
    lines = get_lines("input_10.txt")
    print("Part 1:", part_1(lines))
    print("Part 2:", None)


if __name__ == '__main__':
    main()
