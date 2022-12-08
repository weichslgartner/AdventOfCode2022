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

fn generate_seen_and_blocked(
    grid: Vec<Vec<u32>>,
    mut blocked_by: Vec<Vec<u32>>,
) -> (HashSet<Point>, Vec<Vec<u32>>) {
    let x_max = grid[0].len();
    let y_max = grid.len();
    let mut seen_set = HashSet::new();
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
                    add_to_seen(&neighbors, &grid, &cur, &mut seen_set);
                    update_blocked_by(&neighbors, &grid, &cur, &mut blocked_by);
                } else {
                    seen_set.insert(cur.clone());
                    blocked_by[cur.y][cur.x] = 0;
                }
                neighbors.push(cur);
            }
        }
    }
    (seen_set, blocked_by)
}

fn update_blocked_by(
    neighbors: &[Point],
    grid: &[Vec<u32>],
    cur: &Point,
    blocked_by: &mut [Vec<u32>],
) {
    let mut blocked_n = 0;
    for n in neighbors.iter().rev() {
        blocked_n += 1;
        if grid[n.y][n.x] >= grid[cur.y][cur.x] {
            break;
        }
    }
    blocked_by[cur.y][cur.x] *= blocked_n
}

fn add_to_seen(neighbors: &[Point], grid: &[Vec<u32>], cur: &Point, seen_set: &mut HashSet<Point>) {
    if neighbors
        .iter()
        .cloned()
        .all(|n: Point| grid[cur.y][cur.x] > grid[n.y][n.x])
    {
        seen_set.insert(cur.clone());
    }
}

fn part1(seen_set: HashSet<Point>) -> usize {
    seen_set.len()
}

fn part2(blocked_by: &[Vec<u32>]) -> u32 {
    *blocked_by.iter().flat_map(|x| x.iter()).max().unwrap()
}

fn main() {
    let input = include_str!("../../../inputs/input_08.txt");
    let (grid, blocked) = parse(input);
    let (seen_set, blocked_by) = generate_seen_and_blocked(grid, blocked);
    println!("Part 1: {}", part1(seen_set));
    println!("Part 2: {}", part2(&blocked_by));
}
