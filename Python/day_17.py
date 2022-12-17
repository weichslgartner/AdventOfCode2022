from aoc import *

WIDTH = 7
shapes = [[Point(x=x, y=0) for x in range(4)],
          [Point(x=1, y=0)] + [Point(x=x, y=1) for x in range(3)] + [Point(x=1, y=2)],
          [Point(x=x, y=0) for x in range(3)] + [Point(x=2, y=y) for y in range(1, 3)],
          [Point(x=0, y=y) for y in range(4)],
          [Point(x=x, y=y) for y in range(2) for x in range(2)]
          ]


def parse_input(lines):
    return lines


def move(shape,ground,points, c):
    if c == '>':
        if max(shape, key=lambda p: p.x).x >= WIDTH - 1:
            return shape
        new_shape = [Point(x=p.x + 1, y=p.y) for p in shape]
        for p in new_shape:
            if p in points:
                return shape
        return new_shape
    if c == '<':
        if min(shape, key=lambda p: p.x).x <= 0:
            return shape
        new_shape = [Point(x=p.x - 1, y=p.y) for p in shape]
        for p in new_shape:
            if p in points:
                return shape
        return new_shape
    if c == 'v':
        return [Point(x=p.x, y=p.y - 1) for p in shape]


def hit_ground(ground, shape, points):
    for p in shape:
        if ground[p.x] == p.y - 1 or Point(p.x,p.y-1) in points:
            return True
    return False


def part_1(line, rounds=2022):
    print(shapes)
    j = 0
    points = set()
    ground = [0 for _ in range(WIDTH)]
    for i in range(rounds):
        shape = shapes[i % len(shapes)]
        offset = Point(x=2, y=max(ground) + 4)
        shape = [Point(p.x + offset.x, p.y + offset.y) for p in shape]
        while True:
            c = line[j % len(line)]
            j += 1
            shape = move(shape,ground,points, c)
            if hit_ground(ground, shape,points):
                for p in shape:
                    points.add(p)
                    ground[p.x] = max(ground[p.x], p.y)
               # print("===")
               # print_grid(ground, points)
                break
            else:
                shape = move(shape,ground,points, 'v')
    return max(ground)


def print_grid(ground, points):
    for y in reversed(range(max(ground) + 1)):
        for x in range(WIDTH):
            p = Point(x, y)
            if p in points:
                print('#', end="")
            else:
                print('.', end="")
        print()
    print()


def part_2(lines):
    pass


def main():
    lines = get_lines("input_17.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines[0]))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
