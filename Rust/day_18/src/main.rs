use std::collections::HashSet;
use std::iter::FromIterator;

#[derive(Eq, Hash, PartialEq, Clone, Copy, Debug)]
struct Point3 {
    x: i32,
    y: i32,
    z: i32,
}

fn get_neighbours_3d(p: &Point3) -> [Point3; 6] {
    [
        Point3 {
            x: p.x + 1,
            y: p.y,
            z: p.z,
        },
        Point3 {
            x: p.x - 1,
            y: p.y,
            z: p.z,
        },
        Point3 {
            x: p.x,
            y: p.y + 1,
            z: p.z,
        },
        Point3 {
            x: p.x,
            y: p.y - 1,
            z: p.z,
        },
        Point3 {
            x: p.x,
            y: p.y,
            z: p.z + 1,
        },
        Point3 {
            x: p.x,
            y: p.y,
            z: p.z - 1,
        },
    ]
}

fn parse_input(lines: &str) -> HashSet<Point3> {
    HashSet::from_iter(lines.lines().map(|line| {
        let mut coords = line.splitn(3, ',').map(|s| s.parse().unwrap());
        Point3 {
            x: coords.next().unwrap(),
            y: coords.next().unwrap(),
            z: coords.next().unwrap(),
        }
    }))
}

fn calc_surface(points: &HashSet<Point3>) -> i32 {
    points
        .iter()
        .map(|p| {
            6 - get_neighbours_3d(p)
                .iter()
                .filter(|n| points.contains(n))
                .count() as i32
        })
        .sum()
}

fn find_empty_neighbors(points: &HashSet<Point3>) -> HashSet<Point3> {
    points.iter().fold(HashSet::new(), |mut free_neighbors, p| {
        free_neighbors.extend(
            get_neighbours_3d(p)
                .into_iter()
                .filter(|n| !points.contains(n)),
        );
        free_neighbors
    })
}

fn fill_holes(holes: HashSet<Point3>, points: &mut HashSet<Point3>) {
    points.extend(holes);
}

fn find_holes(
    empty_neighbors: &HashSet<Point3>,
    max_p: &Point3,
    min_p: &Point3,
    points: &HashSet<Point3>,
) -> HashSet<Point3> {
    let mut holes: HashSet<Point3> = HashSet::new();
    empty_neighbors.iter().for_each(|f_n| {
        if !holes.contains(f_n) {
            let (is_outer, visited) = is_outer_surface(f_n, points, min_p, max_p);
            if !is_outer {
                holes.extend(visited);
            }
        }
    });
    holes
}

fn find_limits(points: &HashSet<Point3>) -> (Point3, Point3) {
    let (min_x, min_y, min_z, max_x, max_y, max_z) = points.iter().fold(
        (
            i32::max_value(),
            i32::max_value(),
            i32::max_value(),
            i32::min_value(),
            i32::min_value(),
            i32::min_value(),
        ),
        |(min_x, min_y, min_z, max_x, max_y, max_z), p| {
            (
                min_x.min(p.x),
                min_y.min(p.y),
                min_z.min(p.z),
                max_x.max(p.x),
                max_y.max(p.y),
                max_z.max(p.z),
            )
        },
    );

    (
        Point3 {
            x: max_x,
            y: max_y,
            z: max_z,
        },
        Point3 {
            x: min_x,
            y: min_y,
            z: min_z,
        },
    )
}

fn is_outer_surface(
    point: &Point3,
    points: &HashSet<Point3>,
    min_p: &Point3,
    max_p: &Point3,
) -> (bool, HashSet<Point3>) {
    let mut stack = vec![*point];
    let mut visited = HashSet::new();
    while let Some(cur) = stack.pop() {
        if cur.x > max_p.x
            || cur.y > max_p.y
            || cur.z > max_p.z
            || cur.x < min_p.x
            || cur.y < min_p.y
            || cur.z < min_p.z
        {
            return (true, visited);
        }
        visited.insert(cur);
        get_neighbours_3d(&cur)
            .into_iter()
            .filter(|n| !points.contains(n) && !visited.contains(n))
            .for_each(|n| stack.push(n));
    }
    (false, visited)
}

fn part1(points: &HashSet<Point3>) -> i32 {
    calc_surface(points)
}

fn part2(points: &mut HashSet<Point3>) -> i32 {
    let (max_p, min_p) = find_limits(points);
    let empty_neighbors = find_empty_neighbors(points);
    let holes = find_holes(&empty_neighbors, &max_p, &min_p, points);
    fill_holes(holes, points);
    calc_surface(points)
}

fn main() {
    let input = include_str!("../../../inputs/input_18.txt");
    let mut points = parse_input(input);
    println!("Part 1: {}", part1(&points));
    println!("Part 2: {}", part2(&mut points));
}
