fn parse(input: &str) -> (Vec<Vec<char>>, Vec<Vec<usize>>) {
    let mut stacks: Vec<Vec<char>> = Vec::with_capacity(1);
    for line in input.lines().filter(|x| x.contains('[')) {
        for (idx, c) in line.chars().enumerate() {
            if idx < stacks.len() + 1 {
                stacks.push(Vec::new());
            }
            if c.is_ascii_alphabetic() {
                stacks[idx].push(c);
            }
        }
    }

    (
        stacks.into_iter().filter(|b| !b.is_empty()).collect(),
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
            .collect(),
    )
}

fn part1(stacks: &mut Vec<Vec<char>>, moves: &Vec<Vec<usize>>) -> String {
    moves.into_iter().for_each(|m| {
        let times = m[0];
        let src = m[1];
        let dst = m[2];
        for _ in 0..times {
            let el = stacks[src - 1].pop().unwrap();
            stacks[dst - 1].push(el);
        }
    });
    let mut result = String::new();
    for s in stacks {
        result.push(s[s.len() - 1]);
    }
    result
}

fn part2(stacks: &mut Vec<Vec<char>>, moves: &Vec<Vec<usize>>) -> String {
    moves.into_iter().for_each(|m| {
        let times = m[0];
        let src = m[1];
        let dst = m[2];
        let mut elements: Vec<char> = vec![];
        for _ in 0..times {
            elements.push(stacks[src - 1].pop().unwrap());
        }

        elements.reverse();
        for e in elements {
            stacks[dst - 1].push(e);
        }
    });
    let mut result = String::new();
    for s in stacks {
        result.push(s[s.len() - 1]);
    }
    result
}

fn main() {
    let input = include_str!("../../../inputs/input_05.txt");
    let (mut stacks, moves) = parse(input);
    println!("Part 1: {}", part1(&mut stacks.clone(), &moves));
    println!("Part 2: {}", part2(&mut stacks, &moves));
}
