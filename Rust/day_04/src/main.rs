use std::mem;
type OverlapFun = fn(&[i32], &[i32]) -> bool;

fn line_to_int(input: &str, splitchar: char) -> Vec<i32> {
    input.split(splitchar).map(|x| x.parse().unwrap()).collect()
}

fn parse_input(input: &str) -> Vec<Vec<Vec<i32>>> {
    input
        .lines()
        .into_iter()
        .map(|x| x.split(','))
        .map(|x| x.map(|y| line_to_int(y, '-')).collect())
        .collect()
}

fn complete_overlap(p1: &[i32], p2: &[i32]) -> bool {
    (p2[1] <= p1[1] && p2[0] >= p1[0]) || (p1[1] <= p2[1] && p1[0] >= p2[0])
}

fn partial_overlap(p1: &[i32], p2: &[i32]) -> bool {
    let mut smaller = p1;
    let mut bigger = p2;
    if bigger[0] < smaller[0] {
        mem::swap(&mut smaller, &mut bigger);
    }
    if bigger[0] <= smaller[1] {
        return true;
    }
    false
}

fn solve(input: &[Vec<Vec<i32>>], overlap: OverlapFun) -> usize {
    input
        .iter()
        .filter(|x| overlap(&x[0], &x[1]))
        .count()
   
}

fn part1(input: &[Vec<Vec<i32>>]) -> usize {
    solve(input, complete_overlap)
}

fn part2(input: &[Vec<Vec<i32>>]) -> usize {
    solve(input, partial_overlap)
}

fn main() {
    let input = include_str!("../../../inputs/input_04.txt");
    let pairs = parse_input(input);
    println!("Part 1: {}", part1(&pairs));
    println!("Part 2: {}", part2(&pairs));
}
