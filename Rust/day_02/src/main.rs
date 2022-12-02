const WIN: [&str; 3] = ["A Y", "B Z", "C X"];
const DRAW: [&str; 3] = ["A X", "B Y", "C Z"];
const LOSE: [&str; 3] = ["A Z", "B X", "C Y"];

fn base_points(to_check: char) -> i32 {
    match to_check {
        'X' => 1,
        'Y' => 2,
        'Z' => 3,
        _ => unreachable!(),
    }
}

fn convert(line: &str) -> Option<&&str> {
    match line.chars().nth(2).unwrap() {
        'X' => LOSE
            .iter()
            .find(|x| line.chars().next().unwrap() == x.chars().next().unwrap()),
        'Y' => DRAW
            .iter()
            .find(|x| line.chars().next().unwrap() == x.chars().next().unwrap()),
        'Z' => WIN
            .iter()
            .find(|x| line.chars().next().unwrap() == x.chars().next().unwrap()),
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
        .map(|x: &str| -> &str {
            if part2 {
                return convert(x).unwrap();
            }
            x
        })
        .fold(0, |a: i32, x| a + calc_points(x))
}

fn part1(input: &str) -> i32 {
    solve(input, false)
}

fn part2(input: &str) -> i32 {
    solve(input, true)
}

fn main() {
    let input = include_str!("../../../inputs/input_02.txt").trim();
    println!("Part 1: {}", part1(input));
    println!("Part 2: {}", part2(input));
}
