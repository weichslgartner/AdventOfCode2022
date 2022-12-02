from aoc import get_lines

points = { 'X': 1, 'Y':2, 'Z' : 3}

second = { 'X': 0, 'Y':3, 'Z' : 6}

win = ["A Y", "B Z", "C X"]
draw = ["A X", "B Y", "C Z"]
lose = ["A Z", "B X", "C Y"]

def parse_input(lines):
    return lines


def part_1(lines):
    score = 0
    for line in lines:
        score += points[line[-1]]
        if line in win:
            score +=6
        elif line in draw:
            score += 3
    return score


def part_2(lines):
    score = 0
    for line in lines:
        score += second[line[-1]]
        if second[line[-1]] == 0:
            cur = list(filter(lambda x: x[0]==line[0],lose))[0]
        elif  second[line[-1]] == 3:
            cur = list(filter(lambda x: x[0]==line[0],draw))[0]
        else:
            cur = list(filter(lambda x: x[0]==line[0],win))[0]
        score += points[cur[-1]]
    return score


def main():
    lines = get_lines("input_02.txt")
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
