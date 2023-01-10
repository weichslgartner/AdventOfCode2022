use enum_iterator::{all, Sequence};
use int_enum::IntEnum;

use std::collections::{HashMap, HashSet};
#[repr(u8)]
#[derive(Copy, Clone, PartialEq, Eq, Hash, Debug, Sequence, IntEnum)]
enum Dir {
    North = 0,
    South = 1,
    West = 2,
    East = 3,
}

#[derive(Copy, Clone, PartialEq, Eq, Hash, Debug)]
struct Point {
    x: i32,
    y: i32,
}

fn parse_input(lines: &str) -> HashSet<Point> {
    let mut elves = HashSet::new();
    for (y, line) in lines.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                elves.insert(Point {
                    x: x as i32,
                    y: y as i32,
                });
            }
        }
    }
    elves
}

fn dir2points(cur: Point, direct: Dir) -> Vec<Point> {
    match direct {
        Dir::North => (-1..=1)
            .map(|i| Point {
                x: cur.x + i,
                y: cur.y - 1,
            })
            .collect(),
        Dir::South => (-1..=1)
            .map(|i| Point {
                x: cur.x + i,
                y: cur.y + 1,
            })
            .collect(),
        Dir::West => (-1..=1)
            .map(|i| Point {
                x: cur.x - 1,
                y: cur.y + i,
            })
            .collect(),
        Dir::East => (-1..=1)
            .map(|i| Point {
                x: cur.x + 1,
                y: cur.y + i,
            })
            .collect(),
    }
}

fn get_neighbours_8(p: Point) -> Vec<Point> {
    (-1..=1)
        .flat_map(|y| (-1..=1).map(move |x| (x, y)))
        .filter(|(x, y)| *x != 0 || *y != 0)
        .map(|(x, y)| Point {
            x: p.x + x,
            y: p.y + y,
        })
        .collect()
}

fn solve(mut elves: HashSet<Point>, rounds: i32) -> i32 {
    let mut moves = HashMap::new();
    let mut move_cnt = HashMap::new();
    let mut new_elves = HashSet::new();
    for i in 0..rounds {
        determine_moves(i as usize, &elves, &mut move_cnt, &mut moves);
        // part 2 exit if no movement
        if moves.is_empty() {
            return i + 1;
        }
        move_elves(&mut elves, &move_cnt, &moves, &mut new_elves);
    }
    cnt_empty_space(&elves)
}

fn determine_moves(
    d_offset: usize,
    elves: &HashSet<Point>,
    move_cnt: &mut HashMap<Point, i32>,
    moves: &mut HashMap<Point, Point>,
) {
    move_cnt.clear();
    moves.clear();
    for elf in elves {
        if get_neighbours_8(*elf).iter().all(|n| !elves.contains(n)) {
            continue;
        }
        for d in all::<Dir>() {
            let neighbours = dir2points(
                *elf,
                Dir::from_int(((d.int_value() as usize + d_offset) % all::<Dir>().count()) as u8)
                    .unwrap(),
            );
            if neighbours.iter().all(|n| !elves.contains(n)) {
                moves.insert(*elf, neighbours[1]);
                move_cnt
                    .entry(neighbours[1])
                    .and_modify(|c| *c += 1)
                    .or_insert(1);
                break;
            }
        }
    }
}

fn move_elves(
    elves: &mut HashSet<Point>,
    move_cnt: &HashMap<Point, i32>,
    moves: &HashMap<Point, Point>,
    new_elves: &mut HashSet<Point>,
) {
    new_elves.clear();
    for elf in elves.iter() {
        if moves.contains_key(elf) && *move_cnt.get(moves.get(elf).unwrap()).unwrap() == 1 {
            new_elves.insert(moves[elf]);
        } else {
            new_elves.insert(*elf);
        }
    }
    std::mem::swap(elves, new_elves);
}

fn cnt_empty_space(elves: &HashSet<Point>) -> i32 {
    let minx = elves.iter().min_by_key(|p| p.x).unwrap().x;
    let maxx = elves.iter().max_by_key(|p| p.x).unwrap().x;
    let miny = elves.iter().min_by_key(|p| p.y).unwrap().y;
    let maxy = elves.iter().max_by_key(|p| p.y).unwrap().y;
    (miny..=maxy)
        .map(|y| {
            (minx..=maxx)
                .filter(|&x| !elves.contains(&Point { x, y }))
                .count() as i32
        })
        .sum()
}

fn part1(elves: HashSet<Point>) -> i32 {
    solve(elves, 10)
}

fn part2(elves: HashSet<Point>) -> i32 {
    solve(elves, i32::MAX)
}

fn main() {
    let input = include_str!("../../../inputs/input_23.txt");
    let elves = parse_input(input);
    println!("Part 1: {}", part1(elves.clone()));
    println!("Part 2: {}", part2(elves));
}
