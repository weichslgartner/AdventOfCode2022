use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, HashSet};

#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    point: Point,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other
            .cost
            .cmp(&self.cost)
            .then_with(|| other.point.y.cmp(&self.point.y))
            .then_with(|| other.point.x.cmp(&self.point.x))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

#[derive(Eq, Hash, PartialEq, Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

fn manhattan_distance(a: Point, b: Point) -> i32 {
    ((a.x).abs_diff(b.x) + (a.y).abs_diff(b.y)) as i32
}

fn parse(input: &str) -> (Vec<Vec<u32>>, Point, Point, Point) {
    let max_p = Point {
        x: input.lines().next().unwrap().len() as i32,
        y: input.lines().count() as i32,
    };
    let mut start = Point { x: 0, y: 0 };
    let mut target = Point { x: 0, y: 0 };
    (
        input
            .lines()
            .enumerate()
            .map(|(y, line)| {
                line.chars()
                    .enumerate()
                    .map(|(x, c)| match c {
                        'S' => {
                            start = Point {
                                x: x as i32,
                                y: y as i32,
                            };
                            'a' as u32
                        }
                        'E' => {
                            target = Point {
                                x: x as i32,
                                y: y as i32,
                            };
                            'z' as u32
                        }
                        _ => c as u32,
                    })
                    .collect()
            })
            .collect(),
        start,
        target,
        max_p,
    )
}

fn neighbors(point: Point) -> [Point; 4] {
    [
        Point {
            x: point.x - 1,
            y: point.y,
        },
        Point {
            x: point.x,
            y: point.y - 1,
        },
        Point {
            x: point.x + 1,
            y: point.y,
        },
        Point {
            x: point.x,
            y: point.y + 1,
        },
    ]
}

fn is_in_grid(p: Point, p_max: Point) -> bool {
    (p.x >= 0) && (p.y >= 0) && (p.x < p_max.x) && (p.y < p_max.y)
}

fn a_star(
    grid: &[Vec<u32>],
    start: &Point,
    goal: &Point,
    maxp: &Point,
    is_part_1: bool,
) -> Option<usize> {
    let (mut costs, mut in_queue, mut queue) = init_a_star(grid, goal, start, is_part_1);
    while let Some(State { cost: _, point }) = queue.pop() {
        in_queue.remove(&point);
        if point == *goal {
            return Some(costs[&point]);
        }
        for n in neighbors(point)
            .iter()
            .filter(|p| is_in_grid(**p, *maxp))
            .filter(|p| {
                grid[p.y as usize][p.x as usize] <= grid[point.y as usize][point.x as usize] + 1
            })
        {
            let t_costs = costs[&point] + 1;
            if t_costs < *costs.get(n).unwrap_or(&usize::MAX) {
                costs.insert(*n, t_costs);
                if !in_queue.contains(n) {
                    queue.push(State {
                        cost: t_costs + (manhattan_distance(*n, *goal) as usize),
                        point: *n,
                    });
                    in_queue.insert(*n);
                }
            }
        }
    }
    None
}

fn init_a_star(
    grid: &[Vec<u32>],
    goal: &Point,
    start: &Point,
    is_part_1: bool,
) -> (HashMap<Point, usize>, HashSet<Point>, BinaryHeap<State>) {
    if is_part_1 {
        return (
            HashMap::<Point, usize>::from([(*start, 0)]),
            HashSet::<Point>::from([*start]),
            BinaryHeap::<State>::from([State {
                cost: manhattan_distance(*start, *goal) as usize,
                point: *start,
            }]),
        );
    }

    let start_points = grid.iter().enumerate().flat_map(|(y, line)| {
        line.iter()
            .enumerate()
            .filter(|(_, c)| (**c == 'a' as u32))
            .map(move |(x, _)| Point {
                x: x as i32,
                y: y as i32,
            })
    });

    (
        start_points.clone().map(|p| (p, 0)).collect(),
        start_points.clone().collect(),
        start_points
            .map(|p| State {
                cost: manhattan_distance(p, *goal) as usize,
                point: p,
            })
            .collect(),
    )
}

fn part1(grid: &[Vec<u32>], start: &Point, goal: &Point, maxp: &Point) -> Option<usize> {
    a_star(grid, start, goal, maxp, true)
}

fn part2(grid: &[Vec<u32>], start: &Point, goal: &Point, maxp: &Point) -> Option<usize> {
    a_star(grid, start, goal, maxp, false)
}

fn main() {
    let input = include_str!("../../../inputs/input_12.txt");
    let (grid, start, target, max_p) = parse(input);
    println!("Part 1: {}", part1(&grid, &start, &target, &max_p).unwrap());
    println!("Part 2: {}", part2(&grid, &start, &target, &max_p).unwrap());
}
