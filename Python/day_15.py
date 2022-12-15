from aoc import *


def parse_input(lines):
    pb = []
    for line in lines:
        ints = extract_all_ints(line)
        pb.append([Point(ints[0],ints[1]),Point(ints[2],ints[3])])

    return pb


def part_1(pb,target=2000000):
    free_set = set()
    for sensor, beacon in pb:
        #print(sensor,beacon)
        mh = manhattan_distance(sensor,beacon)
        dist =  mh - manhattan_distance(sensor, Point(sensor.x, target))
        if dist >= 0:
            for x in range(sensor.x-dist,sensor.x+dist+1):
                free_set.add(Point(x,target))

    for sensor, beacon in pb:
        if sensor.y == target:
            free_set.add(sensor)
        if beacon in free_set:
            free_set.remove(beacon)
            print("asd",beacon)
    #print(sorted(free_set))
    return len(free_set)


def part_2(lines):
    pass


def main():
    lines = get_lines("input_15.txt") #too low 4746003 too high 6697770
    pb = parse_input(lines)
    print("Part 1:", part_1(pb))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
