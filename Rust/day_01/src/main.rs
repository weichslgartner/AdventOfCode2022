use std::collections::BinaryHeap;
fn calories_per_elf(input: &str) -> BinaryHeap<i32> {
    input
        .trim()
        .split("\n\n")
        .map(|y| y.split('\n').map(|e| e.parse::<i32>().unwrap()).sum())
        .collect::<BinaryHeap<i32>>()
}

fn part1(input: &BinaryHeap<i32>) -> i32 {
    *input.peek().unwrap()
}

fn part2(input: &mut BinaryHeap<i32>) -> i32 {
    input.drain().take(3).sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_01.txt");
    let mut calories = calories_per_elf(input);
    println!("Part 1: {}", part1(&calories));
    println!("Part 2: {}", part2(&mut calories));
}
