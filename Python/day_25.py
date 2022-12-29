from typing import List

from aoc import get_lines

def to_snafu(val) -> str:
    result = []
    while val != 0:
        remainder = val % 5
        val = val // 5
        if remainder <= 2:
            result.append(str(remainder))
        elif remainder == 3:
            result.append("=")
            val += 1
        elif  remainder == 4:
            result.append("-")
            val += 1
    return ''.join(reversed(result))

def part_1(lines : List[str]):
    global_sum = 0
    for line in lines:
        for i,c in enumerate(line):
            val = 0
            if c.isdigit():
                val = int(c)
            elif c == "=":
                val = -2
            elif c == '-':
                val = -1
            global_sum += 5**(len(line)-i-1)*val
    return to_snafu(global_sum)


def main():
    lines = get_lines("input_25_test.txt")
    print("Part 1:", part_1(lines))


if __name__ == '__main__':
    main()
