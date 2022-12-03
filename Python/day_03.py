from aoc import get_lines
from pathlib import Path


test = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

def parse_input(lines):
    return lines

def part_1(lines):
    res = []
    for line in lines:
        part1 = line[:len(line)//2]
        part2 =  line[len(line)//2:]
        assert(len(part1)==len(part2))
        common = (set(part1) & set(part2)).pop()
        if common.islower():
            res.append(ord(common)- ord('a') + 1)
        else:
            res.append(ord(common)- ord('A') + 27)

    return sum(res)


def part_2(lines):
    res = []
    i =1
    cur_set = set()
    for line in lines:
        if len(cur_set)==0:
            cur_set = set(line)
        else:
            cur_set &= set(line)
        print(i, cur_set)
        if i == 3:
            common = cur_set.pop()
            if common.islower():
                res.append(ord(common) - ord('a') + 1)
            else:
                res.append(ord(common) - ord('A') + 27)
            i=0
        i += 1
    return sum(res)

def main():
    lines = get_lines("input_03.txt")
   # lines = test.splitlines()
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
