import re
from collections import namedtuple
from itertools import filterfalse, tee, islice
from pathlib import Path
from typing import List, Callable, Iterable, Iterator, Any


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.x} {self.y}'


class Point3(namedtuple('Point', 'x y z')):
    def __repr__(self):
        return f'{self.x},{self.y},{self.z}'


def to_point(p: str, sep=",") -> Point:
    p = p.split(sep)
    return Point(int(p[0]), int(p[1]))


def get_neighbours_4(p: Point, p_max: Point) -> Iterator[Point]:
    points = [Point(p.x - 1, p.y), Point(p.x, p.y - 1), Point(p.x + 1, p.y), Point(p.x, p.y + 1)]
    return filter(lambda x: is_in_grid(x, p_max), points)


def get_neighbours_3d(p: Point3) -> List[Point3]:
    return [Point3(p.x - 1, p.y, p.z), Point3(p.x, p.y - 1, p.z), Point3(p.x + 1, p.y, p.z),
            Point3(p.x, p.y + 1, p.z), Point3(p.x, p.y, p.z + 1), Point3(p.x, p.y, p.z - 1)]


def get_neighbours_8(p: Point, p_max: Point) -> Iterator[Point]:
    points = [Point(p.x + x, p.y + y) for y in range(-1, 2) for x in range(-1, 2) if x != 0 or y != 0]
    return filter(lambda n: is_in_grid(n, p_max), points)


def is_in_grid(p: Point, p_max: Point) -> bool:
    return (p.x >= 0) and (p.y >= 0) and (p.x < p_max.x) and (p.y < p_max.y)


def from_grid(p: Point, grid: List[List[int]]) -> int:
    return grid[p.y][p.x]


def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_lines(file_name: str) -> List[str]:
    file = Path(__file__).parents[1] / "inputs" / file_name
    with file.open('r') as f:
        lines = f.read().splitlines()
    return lines


def input_as_str(file_name: str) -> str:
    file = Path(__file__).parents[1] / "inputs" / file_name
    with file.open('r') as f:
        return f.read().strip()


def input_as_str_nostrip(file_name: str) -> str:
    file = Path(__file__).parents[1] / "inputs" / file_name
    with file.open('r') as f:
        return f.read()


def partition(predicate: Callable, iterable: Iterable) -> (Iterable, Iterable):
    t1, t2 = tee(iterable)
    return filterfalse(predicate, t1), filter(predicate, t2)


def take(n, iterable):
    """Return first n items of the iterable as a list"""
    return list(islice(iterable, n))


def chunk(lines: List[Any], size=3) -> List[Any]:
    for i in range(0, len(lines), size):
        yield lines[i:i + size]


def line_to_int(line: str, split_char=",") -> List[int]:
    return [int(i) for i in line.split(split_char) if len(i) > 0]


def extract_all_ints(line: str) -> List[int]:
    return list(map(int, (re.findall(r'-?\d+', line))))
