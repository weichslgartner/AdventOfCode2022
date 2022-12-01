fn calories_per_elf(input: &str) -> Vec<i32> {
    input
        .trim()
        .split("\n\n")
        .map(|y| y.split('\n').map(|e| e.parse::<i32>().unwrap()).sum())
        .collect::<Vec<i32>>()
}

fn part1(input: &Vec<i32>) -> i32 {
    *input.iter().max().unwrap()
}

fn part2(input: &mut Vec<i32>) -> i32 {
    // if partial sort existed, would be better here
    input.sort_unstable_by(|a, b| b.cmp(a));
    input[0..3].iter().sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_01.txt");
    let mut calories = calories_per_elf(input);
    println!("Part 1: {}", part1(&calories));
    println!("Part 2: {}", part2(&mut calories));
}
