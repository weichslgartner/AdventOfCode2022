from typing import List, Tuple

from aoc import get_lines


def solve(lines: List[str]) -> (int, str):
    cycl_cnt = 1
    signal_strength = 0
    register = 1
    pos = 0
    display = '\n'
    for line in lines:
        tokenz = line.split()
        pos, display = add_pixel(display, pos, register)
        if tokenz[0] == "noop":
            cycl_cnt += 1
        if tokenz[0] == "addx":
            pos, display = add_pixel(display, pos, register)
            signal_strength = cond_inc_signal_strength(cycl_cnt + 1, register, signal_strength)
            cycl_cnt += 2
            register += int(tokenz[1])
        signal_strength = cond_inc_signal_strength(cycl_cnt, register, signal_strength)
    return signal_strength, display


def cond_inc_signal_strength(cycl_cnt: int, register: int, signal_strength: int) -> int:
    if cycl_cnt in range(20, 221, 40):
        signal_strength += cycl_cnt * register
    return signal_strength


def add_pixel(display: str, pos: int, register: int) -> Tuple[int, str]:
    if pos in range(register - 1, register + 2):
        display += '#'
    else:
        display += '.'
    if pos == 39:
        display += '\n'
        return 0, display
    return pos + 1, display


def main():
    lines = get_lines("input_10.txt")
    signal_streng, display = solve(lines)
    print("Part 1:", signal_streng)
    print("Part 2:", display)


if __name__ == '__main__':
    main()
