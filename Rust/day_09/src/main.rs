use std::collections::{HashMap, HashSet};

#[derive(Eq, Hash, PartialEq, Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}
fn parse(input: &str) -> Vec<(char, u32)> {
    input
        .lines()
        .map(|l| l.splitn(2, ' '))
        .map(|mut e| {
            (
                e.next().unwrap().chars().next().unwrap(),
                e.next().unwrap().parse().unwrap(),
            )
        })
        .collect()
}

fn part1(commands: &Vec<(char, u32)>) -> usize {
    solve(commands, 2)
}

fn part2(commands: &Vec<(char, u32)>) -> usize {
    solve(commands, 10)
}

fn get_neighbours_8(p: Point) -> HashSet<Point> {
    (-1..=1)
        .flat_map(|x| (-1..=1).map(move |y| (x, y)))
        .filter(|x| x.0 != 0 || x.1 != 0)
        .map(|(x, y)| Point {
            x: p.x + x,
            y: p.y + y,
        })
        .collect()
}

fn dir_to_point(direction: char) -> Point {
    match direction {
        'R' => Point { x: 1, y: 0 },
        'L' => Point { x: -1, y: 0 },
        'U' => Point { x: 0, y: 1 },
        'D' => Point { x: 0, y: -1 },
        _ => unreachable!(),
    }
}

fn sign(x: i32) -> i32 {
    if x == 0 {
        return 0;
    }
    if x < 0 {
        return -1;
    }
    1
}

fn solve(commands: &Vec<(char, u32)>, length: usize) -> usize {
    let mut positions: HashMap<usize, Point> =
        (0..length).map(|i| (i, Point { x: 0, y: 0 })).collect();
    let mut tail_set = HashSet::new();
    for (direct, steps) in commands {
        let direct_point = dir_to_point(*direct);
        for _ in 0..*steps {
            positions.insert(0, move_head(positions[&0], direct_point));
            move_body_and_tail(&mut positions);
            tail_set.insert(positions[&(length - 1)]);
        }
    }
    tail_set.len()
}

fn move_body_and_tail(positions: &mut HashMap<usize, Point>) {
    for i in 1..positions.len() {
        if !get_neighbours_8(positions[&i]).contains(&positions[&(i - 1)]) {
            let new_pos = Point {
                x: positions[&i].x + sign(positions[&(i - 1)].x - positions[&i].x),
                y: positions[&i].y + sign(positions[&(i - 1)].y - positions[&i].y),
            };
            positions.insert(i, new_pos);
        }
    }
}

fn move_head(head: Point, direct_point: Point) -> Point {
    Point {
        x: head.x + direct_point.x,
        y: head.y + direct_point.y,
    }
}

fn main() {
    let input = include_str!("../../../inputs/input_09.txt");
    let commands = parse(input);
    println!("Part 1: {}", part1(&commands));
    println!("Part 2: {}", part2(&commands));
}
