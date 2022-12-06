use std::collections::{HashMap, VecDeque};

fn solve(input: &str, window_size: usize) -> usize {
    let mut deq = VecDeque::new();
    let mut char_cnt= HashMap::with_capacity(window_size);
    for (idx, c) in input.chars().enumerate() {
        char_cnt.entry(c).and_modify(|val| *val += 1).or_insert(1);
        deq.push_back(c);
        if deq.len() > window_size {
            let to_remove = deq.pop_front().unwrap();
            char_cnt.entry(to_remove).and_modify(|val| *val -= 1);
            if char_cnt[&to_remove] == 0 {
                char_cnt.remove(&to_remove);
            }
        }
        if char_cnt.len() == window_size {
            return idx + 1;
        }
    }
    0
}

fn part1(input: &str) -> usize {
    solve(input, 4)
}

fn part2(input: &str) -> usize {
    solve(input, 14)
}

fn main() {
    let input = include_str!("../../../inputs/input_06.txt");
    println!("Part 1: {}", part1(input));
    println!("Part 2: {}", part2(input));
}
