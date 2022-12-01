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

fn part1(input: &str) -> i32 {
    let parsed = input.split("\n\n").collect::<Vec<&str>>();
    let res: i32 = parsed.into_iter().map(|y| parse_element(y)).max().unwrap();
    return res;
}

fn part2(input: &str) -> i32 {
    let mut res: Vec<i32> = parse(input);
    res.sort();
    res.reverse();
    res[0..3].iter().sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_01.txt").trim_end();
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
