const WIN: [&str; 3] = ["A Y", "B Z", "C X"];
const DRAW: [&str; 3] = ["A X", "B Y", "C Z"];
const LOSE: [&str; 3] = ["A Z", "B X", "C Y"];

fn base_points(to_check: char) -> i32 {
    match to_check {
        'X' => return 1,
        'Y' => return 2,
        'Z' => return 3,
        _ => return 0,
    }
}

fn convert(line: &str) -> &str {
    match line.chars().nth(2).unwrap() {
        'X' => {
            return LOSE
                .iter()
                .filter(|x| line.chars().nth(0).unwrap() == x.chars().nth(0).unwrap())
                .next()
                .unwrap()
        }
        'Y' => {
            return DRAW
                .iter()
                .filter(|x| line.chars().nth(0).unwrap() == x.chars().nth(0).unwrap())
                .next()
                .unwrap()
        }
        'Z' => {
            return WIN
                .iter()
                .filter(|x| line.chars().nth(0).unwrap() == x.chars().nth(0).unwrap())
                .next()
                .unwrap()
        }
        _ => return "",
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


fn part1(input: &str) -> i32 {
    input.split('\n').into_iter().fold(0, |a: i32, x: &str| {
        a + base_points(x.chars().nth(2).unwrap()) + win_points(x)
    })
}

fn part2(input: &str) -> i32 {
    input
        .split('\n')
        .into_iter()
        .map(|x| convert(&x))
        .fold(0, |a: i32, x: &str| {
            a + base_points(x.chars().nth(2).unwrap()) + win_points(x)
        })
}

fn main() {
    let input = include_str!("../../../inputs/input_02.txt").trim();
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
