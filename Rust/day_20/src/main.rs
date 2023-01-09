const DECRYPTION_KEY: i64 = 811589153;

fn parse_input(lines: &str) -> Vec<(usize, i64)> {
    lines
        .lines()
        .enumerate()
        .map(|(index, line)| (index, line.parse().unwrap()))
        .collect()
}

fn solve(mut lines: Vec<(usize, i64)>, rounds: usize) -> i64 {
    let length = lines.len();
    let elements = lines.clone();
    for _ in 0..rounds {
        for n in &elements {
            let old_index = lines.iter().position(|x| x == n).unwrap();
            if n.1 == 0 {
                continue;
            }

            let new_index = ((old_index as i64 + n.1).rem_euclid(length as i64 - 1)) as usize;
            let old = lines.remove(old_index);
            lines.insert(new_index, old);
        }
    }
    let idx = lines.iter().position(|x| x.1 == 0).unwrap();
    (1000..=3000)
        .step_by(1000)
        .map(|grove| lines[(idx + grove) % length].1)
        .sum()
}

fn part1(lines: Vec<(usize, i64)>) -> i64 {
    solve(lines, 1)
}

fn part2(lines: Vec<(usize, i64)>) -> i64 {
    let lines = lines
        .into_iter()
        .map(|(index, value)| (index, value * DECRYPTION_KEY))
        .collect();
    solve(lines, 10)
}

fn main() {
    let input = include_str!("../../../inputs/input_20.txt");
    let lines = parse_input(input);
    println!("Part 1: {}", part1(lines.clone()));
    println!("Part 2: {}", part2(lines));
}
