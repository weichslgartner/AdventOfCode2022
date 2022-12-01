fn parse_element(vals: &str) -> i32 {
    vals.split('\n').map(|e| e.parse::<i32>().unwrap()).sum()
}

fn parse(input: &str) -> Vec<i32> {
    input
        .split("\n\n")
        .collect::<Vec<&str>>()
        .into_iter()
        .map(|y| parse_element(y))
        .collect::<Vec<i32>>()
}

fn part1(input: &Vec<i32>) -> i32 {
    *input.iter().max().unwrap()
}

fn part2(input: &mut Vec<i32>) -> i32 {
    input.sort();
    input.reverse();
    input[0..3].iter().sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_01.txt").trim_end();
    let mut parsed_input = parse(input);
    println!("Part 1: {}", part1(&parsed_input));
    println!("Part 2: {}", part2(&mut parsed_input));
}
