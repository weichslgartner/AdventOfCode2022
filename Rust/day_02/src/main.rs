const WIN: [&str; 3] = ["A Y", "B Z", "C X"];
const DRAW: [&str; 3] = ["A X", "B Y", "C Z"];
const LOSE: [&str; 3] = ["A Z", "B X", "C Y"];

fn base_points(to_check: char) -> i32 {
    match to_check {
        'X' => return 1,
        'Y' => return 2,
        'Z' => return 3,
        _ => unreachable!(),
    }
}

fn convert(line: &str) -> &str {
    match line.chars().nth(2).unwrap() {
        'X' => {
            return LOSE
                .iter()
                .find(|x| line.chars().nth(0).unwrap() == x.chars().nth(0).unwrap())
                .unwrap()
        }
        'Y' => {
            return DRAW
                .iter()
                .find(|x| line.chars().nth(0).unwrap() == x.chars().nth(0).unwrap())
                .unwrap()
        }
        'Z' => {
            return WIN
                .iter()
                .find(|x| line.chars().nth(0).unwrap() == x.chars().nth(0).unwrap())
                .unwrap()
        }
        _ => unreachable!(),
    }
}

fn win_points(to_check: &str) -> i32 {
    if WIN.contains(&to_check) {
        return 6;
    }
    if DRAW.contains(&to_check) {
        return 3;
    }
    0
}

fn calc_points(line: &str) -> i32 {
    base_points(line.chars().nth(2).unwrap()) + win_points(line)
}

fn solve(input: &str, part2: bool) -> i32 {
    input
        .split('\n')
        .into_iter()
        .map(|x| {
            if part2 {
                return convert(x);
            }
            return x;
        })
        .fold(0, |a: i32, x: &str| a + calc_points(&x))
}

fn part1(input: &str) -> i32 {
    solve(&input, false)
}

fn part2(input: &str) -> i32 {
    solve(&input, true)
}

fn main() {
    let input = include_str!("../../../inputs/input_02.txt").trim();
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
