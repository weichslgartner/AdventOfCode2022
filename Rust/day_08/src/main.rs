use std::collections::HashSet;

#[derive(Eq, Hash, PartialEq, Debug, Clone)]
struct Point {
    x: usize,
    y: usize,
}

fn to_point(i: usize, j: usize, inverted: bool) -> Point {
    if inverted {
        return Point { x: j, y: i };
    }
    Point { x: i, y: j }
}

fn parse(input: &str) -> (Vec<Vec<u32>>, Vec<Vec<u32>>) {
    (
        input
            .lines()
            .map(|line| line.chars().map(|c| c.to_digit(10).unwrap()).collect())
            .collect(),
        vec![vec![1; input.lines().next().unwrap().len()]; input.lines().count()],
    )
}

fn generate_seen_and_blocked(grid: Vec<Vec<u32>>, mut blocked_by: Vec<Vec<u32>>) -> usize {
    let x_max = grid[0].len();
    let y_max = grid.len();
    let mut seen_set = HashSet::new();
    let bla = (0..10).rev();
    let ranges: [(Vec<usize>, Vec<usize>, bool); 4] = [
        ((0..y_max).collect(), (0..x_max).collect(), false),
        ((0..y_max).collect(), (0..x_max).rev().collect(), false),
        ((0..x_max).collect(), (0..y_max).collect(), true),
        ((0..x_max).collect(), (0..y_max).rev().collect(), true),
    ];
    for (r0, r1, invert) in ranges.iter() {
        for i in r0.iter() {
            let mut neighbors = vec![];
            for j in r1.iter() {
                let cur = to_point(*i, *j, *invert);
                if !neighbors.is_empty() {
                    if neighbors
                        .clone()
                        .into_iter()
                        .all(|n: Point| grid[cur.y][cur.x] > grid[n.y][n.x])
                    {
                        seen_set.insert(cur.clone());
                    }
                } else {
                    seen_set.insert(cur.clone());
                }

                neighbors.push(cur);
            }
        }
    }
    seen_set.len()
    
}

fn part1(input: &str) -> &str {
    input
}

fn part2(input: &str) -> &str {
    input
}

fn main() {
    let input = include_str!("../../../inputs/input_08.txt");
    let (grid, mut blocked) = parse(input);
    let res = generate_seen_and_blocked(grid, blocked);
    println!("Part 1: {}",res);
    println!("Part 2: {}",0);
}
