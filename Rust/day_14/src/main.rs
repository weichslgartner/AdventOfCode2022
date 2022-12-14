use itertools::Itertools;
use std::collections::HashSet;
const START_POINT: Point = Point { x: 500, y: 0 };

#[derive(Eq, Hash, PartialEq, Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

fn parse(input: &str) -> (i32, HashSet<Point>) {
    let points = input
        .lines()
        .map(|line| {
            line.split("->")
                .into_iter()
                .map(|p| p.trim().split_once(','))
                .map(|p| Point {
                    x: p.unwrap().0.parse().unwrap(),
                    y: p.unwrap().1.parse().unwrap(),
                })
                .collect::<Vec<Point>>()
        })
        .collect::<Vec<Vec<Point>>>();
    (
        points
            .clone()
            .into_iter()
            .flatten()
            .max_by_key(|p| p.y)
            .unwrap()
            .y,
        add_rocks(points),
    )
}

fn add_rocks(points: Vec<Vec<Point>>) -> HashSet<Point> {
    let mut rocks = HashSet::new();
    for line in points.iter() {
        line.iter().tuple_windows().for_each(|(p1, p2)| {
            (p1.x.min(p2.x)..=p1.x.max(p2.x)).for_each(|x| {
                rocks.insert(Point { x, y: p1.y });
            });
            (p1.y.min(p2.y)..=p1.y.max(p2.y)).for_each(|y| {
                rocks.insert(Point { x: p1.x, y });
            });
        });
    }
    rocks
}

fn enter_sand(
    rocks: &HashSet<Point>,
    sands: &mut HashSet<Point>,
    maxy: i32,
    last_point: &mut Point,
    is_part1: bool,
) -> bool {
    let mut sand_p = if !sands.contains(last_point) {
        *last_point
    } else {
        START_POINT
    };
    loop {
        if sand_p.y > maxy {
            if is_part1 {
                return false;
            } else {
                break;
            }
        }
        let down = Point {
            x: sand_p.x,
            y: sand_p.y + 1,
        };
        let down_left = Point {
            x: sand_p.x - 1,
            y: sand_p.y + 1,
        };
        let down_right = Point {
            x: sand_p.x + 1,
            y: sand_p.y + 1,
        };
        if is_free(&down, rocks, sands) {
            *last_point = sand_p;
            sand_p = down;
        } else if is_free(&down_left, rocks, sands) {
            *last_point = sand_p;
            sand_p = down_left;
        } else if is_free(&down_right, rocks, sands) {
            *last_point = sand_p;
            sand_p = down_right;
        } else {
            break;
        }
    }
    sands.insert(sand_p);
    if sand_p == START_POINT {
        return false;
    }
    true
}

fn is_free(pos: &Point, rocks: &HashSet<Point>, sands: &HashSet<Point>) -> bool {
    !rocks.contains(pos) && !sands.contains(pos)
}

fn part1(rocks: &HashSet<Point>, maxy: i32) -> usize {
    let mut sands = HashSet::new();
    let mut last_point = START_POINT;
    while enter_sand(rocks, &mut sands, maxy, &mut last_point, true) {}
    sands.len()
}

fn part2(rocks: &HashSet<Point>, maxy: i32) -> usize {
    let mut sands = HashSet::new();
    let mut last_point = START_POINT;
    while enter_sand(rocks, &mut sands, maxy, &mut last_point, false) {}
    sands.len()
}

fn main() {
    let input = include_str!("../../../inputs/input_14.txt");
    let (max_y, rocks) = parse(input);
    println!("Part 1: {}", part1(&rocks, max_y));
    println!("Part 2: {}", part2(&rocks, max_y));
}
