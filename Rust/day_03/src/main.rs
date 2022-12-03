use std::collections::HashSet;


fn calc_prio(common: char) -> u32 {
    let lower_offset: u32 = 'a'.into();
    let upper_offset: u32 = 'A'.into();
    let c: u32 = common.into();
    if common.is_lowercase() {
        return c - lower_offset + 1;
    }
    c - upper_offset + 27
}

fn split_line_in_half(line: &str) -> (&str, &str) {
    let size = line.len() / 2;
    (&line[..size], &line[size..])
}

//     return sum(map(lambda x: calc_prio((set(x[0]) & set(x[1])).pop()), map(split_line_in_half, lines)))

//     input.split('\n').into_iter().map(split_line_in_half)
//.map(|x| HashSet::from(x[0]).difference(HashSet::from(x[1]))
fn part1(input: &str) -> u32 {
    let mut sum = 0;
    for line in input.split('\n') {
        let (part_a, part_b) = split_line_in_half(line);
        let common = find_common_char(part_a, part_b);
        sum += calc_prio(common.unwrap());
    }
    sum
}

fn find_common_char(part_a: &str, part_b: &str) -> Option<char> {
    let seta = part_a.chars().collect::<HashSet<char>>();
    let setb = part_b.chars().collect::<HashSet<char>>();
    seta.intersection(&setb).next().copied()
   
}

fn part2(_input: &str) -> u32 {
    0
}

fn main() {
    let input = include_str!("../../../inputs/input_03.txt").trim();
    println!("Part 1: {}", part1(input));
    println!("Part 2: {}", part2(input));
}
