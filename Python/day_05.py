from copy import deepcopy

from aoc import get_lines
import re


def parse_input(lines):
    stacks = []
    moves = []
    for line in lines:
        if '[' in line:
            for idx, c in enumerate(line):
                if idx >= len(stacks):
                    stacks.append([])
                if c.isalpha():
                    stacks[idx].append(c)
        if 'move' in line:
            moves.append(list(map(int, (re.findall(r'\d+', line)))))
    stacks = list(filter(lambda l: len(l), stacks))
    [s.reverse() for s in stacks]
    return stacks, moves


def part_1(stacks, moves):
    for times, src, dst in moves:
        for _ in range(times):
            stacks[dst - 1].append(stacks[src - 1].pop())
    return ''.join(s[-1] for s in stacks)


def part_2(stacks, moves):
    for times, src, dst in moves:
        stacks[dst - 1] += stacks[src - 1][-times:]
        stacks[src - 1] = stacks[src - 1][:-times]
    return ''.join(s[-1] for s in stacks)


def main():
    lines = get_lines("input_05.txt")
    stacks, moves = parse_input(lines)
    print("Part 1:", part_1(deepcopy(stacks), moves))  # GFTNRBZPF
    print("Part 2:", part_2(stacks, moves))  # VRQWPDSGP


if __name__ == '__main__':
    main()
