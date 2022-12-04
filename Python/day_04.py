from aoc import get_lines, line_to_int

test = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
3-4,2-4
4-4,4-88"""


def parse_input(lines):
    return list(map(lambda line: [line_to_int(p, '-') for p in line.split(',')], lines))


def complete_overlap(p1, p2):
    return (p2[1] <= p1[1] and p2[0] >= p1[0]) or (p1[1] <= p2[1] and p1[0] >= p2[0])


def partial_overlap(p1, p2):
    if p2[0] < p1[0]:
        p1, p2 = p2, p1
    if p2[0] <= p1[1]:
        return True
    return False


def part_1(pairs):
    return sum(map(lambda p: complete_overlap(p[0], p[1]), pairs))


def part_2(pairs):
    return sum(map(lambda p: partial_overlap(p[0], p[1]), pairs))


def main():
    lines = get_lines("input_04.txt")
    pairs = parse_input(lines)
    print("Part 1:", part_1(pairs))  # 584
    print("Part 2:", part_2(pairs))  # 933


if __name__ == '__main__':
    main()
