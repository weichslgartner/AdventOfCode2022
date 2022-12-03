use itertools::Itertools;
use std::collections::HashSet;

fn calc_prio(common: Option<char>) -> Option<u32> {
    match common {
        Some(common) => {
            let lower_offset: u32 = 'a'.into();
            let upper_offset: u32 = 'A'.into();
            let c: u32 = common.into();
            if common.is_lowercase() {
                return Some(c - lower_offset + 1);
            }
            if common.is_uppercase() {
                return Some(c - upper_offset + 27);
            }
            None
        }
        None => None,
    }
}

fn split_line_in_half(line: &str) -> (&str, &str) {
    let size = line.len() / 2;
    (&line[..size], &line[size..])
}

fn find_common_char(part_a: &str, part_b: &str) -> Option<char> {
    let seta = part_a.chars().collect::<HashSet<char>>();
    let setb = part_b.chars().collect::<HashSet<char>>();
    seta.intersection(&setb).next().copied()
}

fn part1(input: &str) -> Option<u32> {
    input
        .lines()
        .map(split_line_in_half)
        .map(|x| find_common_char(x.0, x.1))
        .map(calc_prio)
        .sum()
}

fn part2(input: &str) -> Option<u32> {
    input
        .lines()
        .chunks(3)
        .into_iter()
        .map(find_common_char2)
        .map(calc_prio)
        .sum()
}

// itertools::Chunk<std::str::Lines>
// IntoIterator

//
fn find_common_char2<'a, I: Iterator<Item=&'a str>>(mut chunk: I) -> Option<char> {
    let mut seta = chunk.next()?.chars().collect::<HashSet<char>>();
    for c in chunk {
        let setb = c.chars().collect::<HashSet<char>>();
        seta.retain(|e| setb.contains(e))
    }
    seta.iter().next().copied()
}

fn main() {
    let input = include_str!("../../../inputs/input_03.txt").trim();
    println!("Part 1: {}", part1(input).unwrap());
    println!("Part 2: {}", part2(input).unwrap());
}
