from collections import defaultdict

from aoc import input_as_str


def solve(line, window_size=4):
    deque = []
    char_cnt = defaultdict(int)
    for idx, c in enumerate(line):
        char_cnt[c] += 1
        deque.append(c)
        if len(deque) > window_size:
            to_remove = deque.pop(0)
            char_cnt[to_remove] -= 1
            if char_cnt[to_remove] == 0:
                del char_cnt[to_remove]
        if len(char_cnt) == window_size:
            return idx + 1
    # no solution found
    return 0


def part_1(line):
    return solve(line, window_size=4)


def part_2(line):
    return solve(line, window_size=14)


def main():
    line = input_as_str("input_06.txt")
    print("Part 1:", part_1(line))
    print("Part 2:", part_2(line))


if __name__ == '__main__':
    main()
