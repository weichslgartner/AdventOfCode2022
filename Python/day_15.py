from aoc import *


def parse_input(lines):
    return [[Point(ints[0], ints[1]), Point(ints[2], ints[3]), manhattan_distance(Point(ints[0], ints[1]), Point(ints[2], ints[3]))] for ints in map(extract_all_ints, lines)]


def part_1(pb, target=2000000):
    free_set = set()
    for sensor, beacon, mh in pb:
        dist = mh - manhattan_distance(sensor, Point(sensor.x, target))
        if dist >= 0:
            for x in range(sensor.x - dist, sensor.x + dist + 1):
                free_set.add(Point(x, target))
    for sensor, beacon, mh in pb:
        if sensor.y == target:
            free_set.add(sensor)
        if beacon in free_set:
            free_set.remove(beacon)
    return len(free_set)


def is_in_area(sensor, upper, target, mh):
    dist = mh - manhattan_distance(sensor, Point(sensor.x, target))
    if dist < 0:
        return False, 0, 0
    x_min = max(sensor.x - mh, 0)
    x_max = min(sensor.x + mh, upper)
    if x_min > upper or x_max < 0:
        return False, 0, 0
    return True, max(sensor.x - dist, 0), min(sensor.x + dist, upper)


def part_2(pb, upper=4000000):
    for y in range(0, upper + 1):
        x = 0
        while x < upper:
            ranges = []
            for sensor, beacon, mh in pb:
                isin, x_min, x_max = is_in_area(sensor, upper, y, mh)
                if isin:
                    ranges.append([x_min, x_max])
            for x_min, x_max in sorted(ranges):
                if x_min <= x <= x_max:
                    x = x_max
                if x >= upper:
                    break
            if x != upper:
                return (x + 1) * 4000000 + y

    return None


def main():
    lines = get_lines("input_15.txt")
    pb = parse_input(lines)
    print("Part 1:", part_1(pb))  # 4748135
    print("Part 2:", part_2(pb))  # 13743542639657


if __name__ == '__main__':
    main()
