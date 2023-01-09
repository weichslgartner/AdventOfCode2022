from typing import List, Set, Tuple

from aoc import get_lines, Point3, extract_all_ints, get_neighbours_3d


def parse_input(lines: List[str]) -> Set[Point3]:
    return set((Point3(*extract_all_ints(line)) for line in lines))


def calc_surface(points: Set[Point3]) -> int:
    surface = 0
    for p in points:
        surface += 6 - sum(map(lambda n: n in points, get_neighbours_3d(p)))
    return surface


def find_empty_neighbors(points: Set[Point3]) -> Set[Point3]:
    free_neighbors = set()
    for p in points:
        free_neighbors |= set(filter(lambda n: n not in points, get_neighbours_3d(p)))
    return free_neighbors


def fill_holes(holes: Set[Point3], points: Set[Point3]) -> None:
    points |= holes


def find_holes(empty_neighbors: Set[Point3], max_p: Point3, min_p: Point3, points: Set[Point3]):
    holes = set()
    for f_n in empty_neighbors:
        if f_n in holes:
            continue
        is_outer, visited = is_outer_surface(point=f_n, points=points, min_p=min_p, max_p=max_p)
        if not is_outer:
            holes |= visited
    return holes


def find_limits(points: Set[Point3]) -> Tuple[Point3, Point3]:
    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    max_z = max(points, key=lambda p: p.z).z
    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y
    min_z = min(points, key=lambda p: p.z).z
    min_p = Point3(min_x, min_y, min_z)
    max_p = Point3(max_x, max_y, max_z)
    return max_p, min_p


def is_outer_surface(point: Point3, points: Set[Point3], min_p: Point3, max_p: Point3) -> Tuple[bool, Set[Point3]]:
    stack = []
    visited = set()
    stack.append(point)
    while len(stack) > 0:
        cur = stack.pop()
        if cur.x > max_p.x or cur.y > max_p.y or cur.z > max_p.z \
                or cur.x < min_p.x or cur.y < min_p.y or cur.z < min_p.z:
            return True, visited
        visited.add(cur)
        for n in get_neighbours_3d(cur):
            if n not in points and n not in visited:
                stack.append(n)
    return False, visited


def part_1(points: Set[Point3]) -> int:
    return calc_surface(points)


def part_2(points: Set[Point3]) -> int:
    max_p, min_p = find_limits(points)
    empty_neighbors = find_empty_neighbors(points)
    holes = find_holes(empty_neighbors, max_p, min_p, points)
    fill_holes(holes, points)
    return calc_surface(points)


def main():
    lines = get_lines("input_18.txt")
    points = parse_input(lines)
    print("Part 1:", part_1(points))
    print("Part 2:", part_2(points))


if __name__ == '__main__':
    main()
