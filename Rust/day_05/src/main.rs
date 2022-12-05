fn parse(input: &str) -> (Vec<Vec<char>>, Vec<Vec<usize>>) {
    (parse_stacks(input), parse_moves(input))
}

fn parse_stacks(input: &str) -> Vec<Vec<char>> {
    input
        .lines()
        .filter(|x| x.contains('['))
        .fold(vec![Vec::new(); 10], |mut accu, line| {
            line.chars().enumerate().for_each(|(idx, c)| {
                if idx >= accu.len() {
                    accu.push(Vec::new());
                }
                if c.is_ascii_alphabetic() {
                    accu[idx].push(c);
                }
            });
            accu
        })
        .into_iter()
        .filter(|b| !b.is_empty())
        .map(|x| x.into_iter().rev().collect())
        .collect()
}

fn parse_moves(input: &str) -> Vec<Vec<usize>> {
    input
        .lines()
        .filter(|x| x.contains("move"))
        .map(|x| x.split(' '))
        .map(|x| {
            x.into_iter()
                .filter(|x| x.chars().next().unwrap().is_ascii_digit())
                .map(|x| x.parse().unwrap())
                .collect()
        })
        .collect()
}

fn extract_top_name(stacks: &[Vec<char>]) -> String {
    stacks.iter().map(|s| s[s.len() - 1]).collect()
}

fn part1(stacks: &mut [Vec<char>], moves: &[Vec<usize>]) -> String {
    moves.iter().for_each(|m| {
        if let [times, src, dst] = &m[..] {
            for _ in 0..*times {
                let el = stacks[src - 1].pop().unwrap();
                stacks[dst - 1].push(el);
            }
        }
    });
    extract_top_name(stacks)
}

fn part2(stacks: &mut [Vec<char>], moves: &[Vec<usize>]) -> String {
    moves.iter().for_each(|m| {
        if let [times, src, dst] = &m[..] {
            let mut elements: Vec<char> = vec![];
            for _ in 0..*times {
                elements.push(stacks[src - 1].pop().unwrap());
            }

            elements.reverse();
            for e in elements {
                stacks[dst - 1].push(e);
            }
        }
    });
    extract_top_name(stacks)
}

fn main() {
    let input = include_str!("../../../inputs/input_05.txt");
    let (mut stacks, moves) = parse(input);
    println!("Part 1: {}", part1(&mut stacks.clone(), &moves));
    println!("Part 2: {}", part2(&mut stacks, &moves));
}
