use std::cmp::Ordering;
use std::{
    collections::{HashMap, HashSet},
    mem::swap,
    slice::Iter,
};

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub enum Direction {
    UP,
    DOWN,
    RIGHT,
    LEFT,
}

impl Direction {
    pub fn iterator() -> Iter<'static, Direction> {
        static DIRECTIONS: [Direction; 4] = [
            Direction::UP,
            Direction::DOWN,
            Direction::RIGHT,
            Direction::LEFT,
        ];
        DIRECTIONS.iter()
    }
}

#[derive(Eq, Hash, PartialEq, Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Eq, PartialEq, Debug, Clone)]
struct ValleyMap {
    blizzards: HashMap<Direction, HashMap<usize, Vec<i32>>>,
    width: i32,
    height: i32,
    period: i32,
}

#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: i32,
    time: i32,
    point: Point,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other
            .cost
            .cmp(&self.cost)
            .then_with(|| other.time.cmp(&self.time))
            .then_with(|| other.point.y.cmp(&self.point.y))
            .then_with(|| other.point.x.cmp(&self.point.x))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn wrap_around(period: i32, offset: i32, x: i32) -> i32 {
    (x + offset) % period
}

fn wrap_around_neg(period: i32, offset: i32, x: i32) -> i32 {
    (period + offset - (x % period)) % period
}

fn parse(input: &str) -> ValleyMap {
    let width :i32 = input.lines().next().unwrap().len().try_into().unwrap();
    let height: i32 = input.lines().count().try_into().unwrap();
    let blizzards_iter = input
        .lines()
        .enumerate()
        .flat_map(|(y, line)| {
            line.chars().enumerate().map(move |(x, c)| {
                let _p = Point {
                    x: x.try_into().unwrap(),
                    y: y.try_into().unwrap(),
                };
                match c {
                    'v' => Some((Direction::DOWN, x - 1, y as i32 - 1)),
                    '^' => Some((Direction::UP, x - 1, y as i32 - 1)),
                    '>' => Some((Direction::RIGHT, y - 1, x as i32 - 1)),
                    '<' => Some((Direction::LEFT, y - 1, x as i32 - 1)),
                    _ => None,
                }
            })
        })
        .flatten();
    let mut blizzards: HashMap<Direction, HashMap<usize, Vec<i32>>> = HashMap::new();

    for direction in Direction::iterator() {
        let mut blizzards_dir: HashMap<usize, Vec<i32>> = HashMap::new();
        blizzards_iter
            .clone()
            .filter(|(dir, _, _)| *dir == *direction)
            .map(|(_, row, offset)| (row, offset))
            .for_each(|(row, offset)| {
                if let Some(x) = blizzards_dir.get_mut(&row) {
                    x.push(offset);
                } else {
                    blizzards_dir.insert(row, vec![offset]);
                }
            });
        blizzards.insert(*direction, blizzards_dir);
    }
    ValleyMap {
        blizzards,
        width: width - 2,
        height: height - 2,
        period: width * height,
    }
}

fn solve(
    start: Point,
    target: Point,
    init_time: i32,
    valley: &ValleyMap,
    blizzard_map: &HashMap<i32, HashSet<Point>>,
) -> i32 {
    let mut queue: HashSet<Point> = HashSet::new();
    let mut next_set: HashSet<Point> = HashSet::new();
    let mut time = init_time;
    queue.insert(start);
    loop {
        next_set.clear();
        for cur in queue.clone().into_iter() {
            if cur == target {
                return time;
            }

            if cur.y > 0 {
                let p = Point {
                    x: cur.x,
                    y: cur.y - 1,
                };
                if !blizzard_map[&((time + 1) % valley.period)].contains(&p) {
                    next_set.insert(p);
                }
            }
            if cur.y < valley.height - 1 {
                let p = Point {
                    x: cur.x,
                    y: cur.y + 1,
                };
                if !blizzard_map[&((time + 1) % valley.period)].contains(&p) {
                    next_set.insert(p);
                }
            }

            if cur.x > 0 && cur.y < valley.height {
                let p = Point {
                    x: cur.x - 1,
                    y: cur.y,
                };
                if !blizzard_map[&((time + 1) % valley.period)].contains(&p) {
                    next_set.insert(p);
                }
            }
            if cur.x < valley.width - 1 && cur.y >= 0 {
                let p = Point {
                    x: cur.x + 1,
                    y: cur.y,
                };
                if !blizzard_map[&((time + 1) % valley.period)].contains(&p) {
                    next_set.insert(p);
                }
            }
            if cur.x == target.x && cur.y.abs_diff(target.y) == 1 {
                next_set.insert(target);
            }

            if !blizzard_map[&((time + 1) % valley.period)].contains(&cur) {
                next_set.insert(cur);
            }
        }
        time += 1;
        swap(&mut queue, &mut next_set);
    }
}

fn main() {
    let input = include_str!("../../../inputs/input_24.txt");
    let valley = parse(input);
    let blizzard_map: HashMap<i32, HashSet<Point>> = (0..=valley.period)
        .map(|i| (i, get_blizzards(&valley, valley.width, i, valley.height)))
        .collect();
    let start = Point { x: 0, y: -1 };
    let target = Point {
        x: valley.width - 1,
        y: valley.height,
    };
    let time1 = solve(start, target, 0, &valley, &blizzard_map);
    let time2 = solve(target, start, time1, &valley, &blizzard_map);
    let time3 = solve(start, target, time2, &valley, &blizzard_map);
    println!("Part 1: {time1}");
    println!("Part 2: {time3}");
}

fn get_blizzards(
    valley: &ValleyMap,
    row_length: i32,
    i: i32,
    column_length: i32,
) -> HashSet<Point> {
    let mut right: HashSet<_> = valley.blizzards[&Direction::RIGHT]
        .iter()
        .map(|(row, offsets)| {
            offsets
                .iter()
                .map(|offset| Point {
                    x: wrap_around(row_length, *offset, i),
                    y: *row as i32,
                })
                .collect::<HashSet<_>>()
        })
        .fold(HashSet::<Point>::new(), |mut accu, p| {
            accu.extend(&p);
            accu
        });
    let left: HashSet<_> = valley.blizzards[&Direction::LEFT]
        .iter()
        .map(|(row, offsets)| {
            offsets
                .iter()
                .map(|offset| Point {
                    x: wrap_around_neg(row_length, *offset, i),
                    y: *row as i32,
                })
                .collect::<HashSet<_>>()
        })
        .fold(HashSet::<Point>::new(), |mut accu, p| {
            accu.extend(&p);
            accu
        });
    let up: HashSet<_> = valley.blizzards[&Direction::UP]
        .iter()
        .map(|(column, offsets)| {
            offsets
                .iter()
                .map(|offset| Point {
                    x: *column as i32,
                    y: wrap_around_neg(column_length, *offset, i),
                })
                .collect::<HashSet<_>>()
        })
        .fold(HashSet::<Point>::new(), |mut accu, p| {
            accu.extend(&p);
            accu
        });
    let down: HashSet<_> = valley.blizzards[&Direction::DOWN]
        .iter()
        .map(|(column, offsets)| {
            offsets
                .iter()
                .map(|offset| Point {
                    x: *column as i32,
                    y: wrap_around(column_length, *offset, i),
                })
                .collect::<HashSet<_>>()
        })
        .fold(HashSet::<Point>::new(), |mut accu, p| {
            accu.extend(&p);
            accu
        });
    right.extend(&left);
    right.extend(&up);
    right.extend(&down);
    right
}
