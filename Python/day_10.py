from aoc import get_lines
from pathlib import Path
m_points = [20,60,100,140,180,220]

def parse_input(lines):
    return lines


def part_1(lines):
    cycl_cnt = 1
    signal_strength = 0
    register = 1
    for line in lines:
        tokenz = line.split()
        if tokenz[0] == "noop":
            cycl_cnt +=1
        if tokenz[0] == "addx":
            if (cycl_cnt+1) in m_points:
                signal_strength += (cycl_cnt+1) * register
                print("*",cycl_cnt+1, (cycl_cnt+1) * register)

            cycl_cnt += 2
            register += int(tokenz[1])
        if cycl_cnt in m_points:
            signal_strength += cycl_cnt*register
            print(cycl_cnt,cycl_cnt*register)
    return signal_strength

def part_2(lines):
    pass


def main():
    lines = get_lines("input_10.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
