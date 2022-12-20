from aoc import get_lines

decryption_key = 811589153


def parse_input(lines):
    return list(enumerate(map(int, lines)))


def solve(lines, rounds):
    length = len(lines)
    elements = lines.copy()
    for _ in range(rounds):
        for n in elements:
            old_index = lines.index(n)
            i = n[1]
            if i == 0:
                continue
            elif old_index + i < 0 or old_index + i >= length:
                new_index = (old_index + i) % (length - 1)
            else:
                new_index = (old_index + i)
            lines.insert(new_index if new_index else length - 1, lines.pop(old_index))
    idx = lines.index(list(filter(lambda x: x[1] == 0, lines)).pop())
    return sum(map(lambda x: x[1], (lines[(idx + grove) % length] for grove in [1000, 2000, 3000])))


def part_1(lines):
    return solve(lines, 1)


def part_2(lines):
    lines = list(map(lambda x: (x[0], x[1] * decryption_key), lines))
    return solve(lines, 10)


def main():
    lines = get_lines("input_20.txt")  # too low 6711
    lines = parse_input(lines)
    print("Part 1:", part_1(lines.copy()))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
