use lazy_static::lazy_static;
use regex::Regex;

#[derive(Eq, Hash, PartialEq, Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

fn manhattan_distance(a: Point, b: Point) -> i32 {
    ((a.x).abs_diff(b.x) + (a.y).abs_diff(b.y)) as i32
}
fn parse(input: &str) -> Vec<(Point, i32)> {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"-?\d+").unwrap();
    }
    input
        .lines()
        .map(|line| {
            RE.find_iter(line)
                .filter_map(|digits| digits.as_str().parse::<i32>().ok())
                .collect::<Vec<_>>()
        })
        .map(|v| (Point { x: v[0], y: v[1] }, Point { x: v[2], y: v[3] }))
        .map(|(p1, p2)| (p1, manhattan_distance(p1, p2)))
        .collect::<Vec<(Point, i32)>>()
}

fn is_in_area(sensor: Point, upper: Option<i32>, target: i32, mh: i32) -> Option<(i32, i32)> {
    let dist = mh
        - manhattan_distance(
            sensor,
            Point {
                x: sensor.x,
                y: target,
            },
        );
    if dist < 0 {
        return None;
    }
    if let Some(upper) = upper {
        let x_min = 0.max(sensor.x - mh);
        let x_max = upper.min(sensor.x + mh);
        if x_min > upper || x_max < 0 {
            return None;
        }
        return Some((0.max(sensor.x - dist), upper.min(sensor.x + dist)));
    }
    Some((sensor.x - dist, sensor.x + dist))
}

fn get_sorted_ranges(pb: &[(Point, i32)], upper: Option<i32>, y: i32) -> Vec<(i32, i32)> {
    let mut ranges: Vec<_> = pb
        .iter()
        .flat_map(|(sensor, mh)| is_in_area(*sensor, upper, y, *mh))
        .collect();
    ranges.sort();
    ranges
}

fn part1(pb: &[(Point, i32)], target: i32) -> Option<u64> {
    let ranges = get_sorted_ranges(pb, None, target);
    let mut free_spaces: u64 = 0;
    let mut x = None;
    for (x_min, x_max) in ranges {
        match x {
            Some(old_x) => {
                if old_x > x_max {
                    //do nothing
                } else if old_x >= x_min && old_x <= x_max {
                    free_spaces += (x_max - old_x) as u64;
                }
                if old_x < x_max {
                    x = Some(x_max);
                }
            }
            _ => {
                free_spaces += (x_max - x_min) as u64;
                x = Some(x_max)
            }
        }
    }
    Some(free_spaces)
}

fn part2(pb: &[(Point, i32)], upper: i32) -> Option<u64> {
    for y in 0..=upper {
        let mut x = 0;
        let ranges = get_sorted_ranges(pb, Some(upper), y);
        for (x_min, x_max) in ranges {
            if x >= x_min && x <= x_max {
                x = x_max;
            }
            if x >= upper {
                break;
            }
        }
        if x != upper {
            return Some((x + 1) as u64 * 4000000 + y as u64);
        }
    }
    None
}

fn main() {
    let input = include_str!("../../../inputs/input_15.txt");
    let pb = parse(input);
    println!("Part 1: {}", part1(&pb, 2_000_000).unwrap());
    println!("Part 2: {}", part2(&pb, 4_000_000).unwrap());
}
