use itertools::Itertools;
use std::collections::HashSet;

fn calc_prio(common: Option<char>) -> Option<u32> {
    match common {
        Some(common) => {
            let c: u32 = common.into();
            if common.is_lowercase() {
                let lower_offset: u32 = 'a'.into();
                return Some(c - lower_offset + 1);
            }
            if common.is_uppercase() {
                let upper_offset: u32 = 'A'.into();
                return Some(c - upper_offset + 27);
            }
            None
        }
        None => None,
    }
}

fn split_line_in_half(line: &str) -> (&str, &str) {
    (&line[..(line.len() / 2)], &line[(line.len() / 2)..])
}

fn find_common_char<I>(mut chunk: I) -> Option<char>
where
    I: Iterator,
    I::Item: AsRef<str>,
{
    let init = chunk.next()?.as_ref().chars().collect::<HashSet<char>>();
    let sum = chunk.fold(init, |mut accu, x| {
        let setb = x.as_ref().chars().collect::<HashSet<char>>();
        accu.retain(|e| setb.contains(e));
        accu
    });
    sum.iter().next().copied()
}

fn part1(input: &str) -> Option<u32> {
    input
        .lines()
        .map(split_line_in_half)
        .map(|x| find_common_char([x.0, x.1].iter()))
        .map(calc_prio)
        .sum()
}

fn part2(input: &str) -> Option<u32> {
    input
        .lines()
        .chunks(3)
        .into_iter()
        .map(find_common_char)
        .map(calc_prio)
        .sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_03.txt").trim();
    println!("Part 1: {}", part1(input).unwrap());
    println!("Part 2: {}", part2(input).unwrap());
}
