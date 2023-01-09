from typing import List, Set

from Python.aoc import Point, input_as_str

WIDTH = 7
shapes = [[Point(x=x, y=0) for x in range(4)],
          [Point(x=1, y=0)] + [Point(x=x, y=1) for x in range(3)] + [Point(x=1, y=2)],
          [Point(x=x, y=0) for x in range(3)] + [Point(x=2, y=y) for y in range(1, 3)],
          [Point(x=0, y=y) for y in range(4)],
          [Point(x=x, y=y) for y in range(2) for x in range(2)]
          ]


def move(shape: List[Point], points: Set[Point], c: str) -> List[Point]:
    if c == '>':
        if max(shape, key=lambda p: p.x).x >= WIDTH - 1:
            return shape
        new_shape = [Point(x=p.x + 1, y=p.y) for p in shape]
        if any(p in points for p in new_shape):
            return shape
        return new_shape
    if c == '<':
        if min(shape, key=lambda p: p.x).x <= 0:
            return shape
        new_shape = [Point(x=p.x - 1, y=p.y) for p in shape]
        if any(p in points for p in new_shape):
            return shape
        return new_shape
    if c == 'v':
        return [Point(x=p.x, y=p.y - 1) for p in shape]


def hit_ground(ground: List[int], shape: List[Point], points: Set[Point]) -> bool:
    if any(ground[p.x] == p.y - 1 or Point(p.x, p.y - 1) in points for p in shape):
        return True
    return False


def solve(line: str, rounds: int) -> int:
    j = 0
    points = set()
    ground = [0 for _ in range(WIDTH)]
    cycle_detect = {}
    periods = []
    for i in range(rounds):
        shape = shapes[i % len(shapes)]
        offset = Point(x=2, y=max(ground) + 4)
        shape = [Point(p.x + offset.x, p.y + offset.y) for p in shape]
        while True:
            c = line[j]
            j = (j + 1) % len(line)
            shape = move(shape, points, c)
            if hit_ground(ground, shape, points):
                for p in shape:
                    points.add(p)
                    ground[p.x] = max(ground[p.x], p.y)
                top = '-'.join([str(x - min(ground)) for x in ground])
                if top in cycle_detect:
                    to_go = rounds - i - 1
                    period = i - cycle_detect[top][0]
                    periods.append(period)
                    cycles = to_go // period
                    from collections import Counter
                    if to_go % period == 0 and period == Counter(periods).most_common(1)[0][0] and len(periods) > 300:
                        return max(ground) + cycles * (max(ground) - cycle_detect[top][1])
                cycle_detect[top] = (i, max(ground))
                break
            else:
                shape = move(shape, points, 'v')
    return max(ground)


def part_1(line: str) -> int:
    return solve(line, rounds=2022)


def part_2(line: str) -> int:
    return solve(line, rounds=1_000_000_000_000)


def main():
    line = input_as_str("input_17.txt")
    print("Part 1:", part_1(line))
    print("Part 2:", part_2(line))


if __name__ == '__main__':
    main()
