use std::collections::BinaryHeap;
#[derive(Debug, Clone, PartialEq, Copy)]
enum Operand {
    Value(u128),
    Old,
}
impl std::str::FromStr for Operand {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if let Ok(val) = s.parse::<u128>() {
            return Ok(Operand::Value(val));
        }
        Ok(Operand::Old)
    }
}

#[derive(Debug, Clone, Copy)]
#[allow(dead_code)]
struct Operation {
    operand_1: Operand,
    operand_2: Operand,
    operator: char,
}

#[derive(Debug, Clone)]
struct Monkey {
    number: u32,
    items: Vec<u128>,
    operation: Operation,
    div_by: u128,
    if_true: usize,
    if_false: usize,
    inspect_cnt: u128,
}

impl Monkey {
    fn new() -> Self {
        Monkey {
            number: 0,
            items: vec![],
            operation: Operation {
                operand_1: Operand::Old,
                operand_2: Operand::Old,
                operator: '+',
            },
            div_by: 0,
            if_true: 0,
            if_false: 0,
            inspect_cnt: 0,
        }
    }
}

fn parse_monkey(input: &str) -> Monkey {
    let mut monkey = Monkey::new();
    for line in input.split('\n') {
        if line.contains("Monkey") {
            monkey.number = line
                .split_once(' ')
                .unwrap()
                .1
                .replace(':', " ")
                .trim()
                .parse()
                .unwrap();
        } else if line.contains("Operation") {
            let mut tokens = line.split('=').last().unwrap().split(' ');
            monkey.operation.operator = tokens.nth(2).unwrap().chars().next().unwrap();
            monkey.operation.operand_2 = tokens.last().unwrap().parse().unwrap();
        } else if line.contains("Starting items") {
            monkey.items = line
                .split_once(':')
                .unwrap()
                .1
                .split(',')
                .map(|x| x.trim().parse().unwrap())
                .collect();
        } else if line.contains("Test: divisible") {
            monkey.div_by = line.split(' ').last().unwrap().parse().unwrap();
        } else if line.contains("If true:") {
            monkey.if_true = line.split(' ').last().unwrap().parse().unwrap();
        } else if line.contains("If false:") {
            monkey.if_false = line.split(' ').last().unwrap().parse().unwrap();
        }
    }

    monkey
}

fn parse(input: &str) -> Vec<Monkey> {
    let mut monkeys = vec![];
    for monkey_description in input.split("\n\n") {
        monkeys.push(parse_monkey(monkey_description));
    }

    monkeys
}
fn solve(monkeys: &mut Vec<Monkey>, rounds: usize, part2: bool) -> u128 {
    let mod_op: u128 = monkeys.iter().map(|m| m.div_by).product();
    for _ in 0..rounds {
        for i in 0..monkeys.len() {
            monkeys[i].inspect_cnt += monkeys[i].items.len() as u128;
            let mut temp = vec![];
            for item in monkeys[i].items.iter() {
                let mut op2 = *item;
                if let Operand::Value(i) = monkeys[i].operation.operand_2 {
                    op2 = i;
                }
                let mut result = if monkeys[i].operation.operator == '+' {
                    *item + op2
                } else {
                    *item * op2
                };
                result = if part2 { result % mod_op } else { result / 3 };
                let idx = if (result % monkeys[i].div_by) == 0 {
                    monkeys[i].if_true
                } else {
                    monkeys[i].if_false
                };
                temp.push((idx, result));
            }
            temp.iter()
                .for_each(|(idx, result)| monkeys[*idx].items.push(*result));

            monkeys[i].items.clear();
        }
    }

    let mut heap = monkeys
        .iter()
        .map(|x| x.inspect_cnt)
        .collect::<BinaryHeap<_>>();
    heap.pop().unwrap() * heap.pop().unwrap()
}

fn part1(monkeys: &mut Vec<Monkey>) -> u128 {
    solve(monkeys, 20, false)
}

fn part2(monkeys: &mut Vec<Monkey>) -> u128 {
    solve(monkeys, 10_000, true)
}

fn main() {
    let input = include_str!("../../../inputs/input_11.txt");
    let mut monkeys = parse(input);
    println!("Part 1: {}", part1(&mut monkeys.clone()));
    println!("Part 2: {}", part2(&mut monkeys));
}
