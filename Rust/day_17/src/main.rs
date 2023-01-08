use std::collections::{HashMap, HashSet};

const WIDTH: usize = 7;

#[derive(Clone, Eq, Hash, PartialEq, Debug)]
struct Point {
    x: usize,
    y: usize,
}

impl Point {
    fn new(x: usize, y: usize) -> Self {
        Self { x, y }
    }
}

fn most_common_element(numbers: &[usize]) -> usize {
    let frequency_map = numbers.iter().fold(HashMap::new(), |mut acc, x| {
        *acc.entry(*x).or_insert(0) += 1;
        acc
    });
    *frequency_map
        .iter()
        .max_by(|(_, a), (_, b)| a.cmp(b))
        .unwrap()
        .0
}

fn generate_shapes() -> [Vec<Point>; 5] {
    [
        (0..4).map(|x| Point::new(x, 0)).collect(),
        vec![Point::new(1, 0)]
            .into_iter()
            .chain((0..3).map(|x| Point::new(x, 1)))
            .chain(vec![Point::new(1, 2)].into_iter())
            .collect(),
        vec![Point::new(0, 0)]
            .into_iter()
            .chain((1..3).map(|x| Point::new(x, 0)))
            .chain((1..3).map(|y| Point::new(2, y)))
            .collect(),
        (0..4).map(|y| Point::new(0, y)).collect(),
        (0..2)
            .flat_map(|y| (0..2).map(move |x| Point::new(x, y)))
            .collect(),
    ]
}

fn move_shape(shape: Vec<Point>, points: &HashSet<Point>, c: char) -> Vec<Point> {
    match c {
        '>' => {
            let max_x = shape.iter().max_by_key(|p| p.x).unwrap().x;
            if max_x >= WIDTH - 1 {
                return shape;
            }
            let new_shape: Vec<_> = shape.iter().map(|p| Point::new(p.x + 1, p.y)).collect();
            if new_shape.iter().any(|p| points.contains(p)) {
                return shape;
            }
            new_shape
        }
        '<' => {
            let min_x = shape.iter().min_by_key(|p| p.x).unwrap().x;
            if min_x == 0 {
                return shape;
            }
            let new_shape: Vec<_> = shape.iter().map(|p| Point::new(p.x - 1, p.y)).collect();
            if new_shape.iter().any(|p| points.contains(p)) {
                return shape;
            }
            new_shape
        }
        'v' => shape.iter().map(|p| Point::new(p.x, p.y - 1)).collect(),
        _ => shape,
    }
}

fn hit_ground(ground: &[usize], shape: &[Point], points: &HashSet<Point>) -> bool {
    shape
        .iter()
        .any(|p| ground[p.x] == p.y - 1 || points.contains(&Point::new(p.x, p.y - 1)))
}

fn solve(line: &str, rounds: usize) -> usize {
    let mut j = 0;
    let mut points: HashSet<Point> = HashSet::new();
    let mut ground = vec![0; WIDTH];
    let mut cycle_detect: HashMap<String, (usize, usize)> = HashMap::new();
    let mut periods: Vec<usize> = Vec::new();
    let shapes = generate_shapes();
    for i in 0..rounds {
        let mut shape = shapes[i % shapes.len()].clone();
        let offset = Point::new(2, ground.iter().max().unwrap() + 4);
        shape = shape
            .iter()
            .map(|p| Point::new(p.x + offset.x, p.y + offset.y))
            .collect();
        loop {
            let c = line.chars().nth(j).unwrap();
            j = (j + 1) % line.len();
            shape = move_shape(shape, &points, c);
            if hit_ground(&ground, &shape, &points) {
                for p in shape.iter() {
                    points.insert(p.clone());
                    ground[p.x] = ground[p.x].max(p.y);
                }
                let top: String = ground
                    .iter()
                    .enumerate()
                    .map(|(_i, x)| x - ground.iter().min().unwrap())
                    .map(|x| x.to_string())
                    .collect::<Vec<String>>()
                    .join("-");
                if cycle_detect.contains_key(&top) {
                    let to_go = rounds - i - 1;
                    let period = i - cycle_detect[&top].0;
                    periods.push(period);
                    let cycles = to_go / period;
                    if to_go % period == 0
                        && period == most_common_element(&periods)
                        && periods.len() > 300
                    {
                        return ground.iter().max().unwrap()
                            + cycles * (*ground.iter().max().unwrap() - cycle_detect[&top].1);
                    }
                }
                cycle_detect.insert(top, (i, *ground.iter().max().unwrap()));
                break;
            } else {
                shape = move_shape(shape, &points, 'v');
            }
        }
    }
    *ground.iter().max().unwrap()
}

fn part1(input: &str) -> usize {
    solve(input, 2022)
}

fn part2(input: &str) -> usize {
    solve(input, 1000000000000)
}

fn main() {
    let input = include_str!("../../../inputs/input_17.txt").trim();
    println!("Part 1: {}", part1(input));
    println!("Part 2: {}", part2(input));
}
