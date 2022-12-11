use std::collections::BinaryHeap;
#[derive(Debug, Clone, PartialEq, Copy)]
enum Operand {
    Value(i64),
    Old,
}
impl std::str::FromStr for Operand {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if let Ok(val) = s.parse::<i64>() {
            return Ok(Operand::Value(val));
        }
        return Ok(Operand::Old);
    }
}

#[derive(Debug, Clone, Copy)]
struct Operation {
    operand_1: Operand,
    operand_2: Operand,
    operator: char,
}

#[derive(Debug, Clone)]
struct Monkey {
    number: u32,
    items: Vec<i64>,
    operation: Operation,
    div_by: i64,
    if_true: usize,
    if_false: usize,
    inspect_cnt: usize,
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

// for line in lines:
// if "Monkey" in line:
//     new_monkey = Monkey(number=extract_all_ints(line).pop())
// elif "Starting items" in line:
//     new_monkey.items = [x for x in extract_all_ints(line)]
// elif "Operation" in line:
//     tokens = line.split('=')[1].split()
//     new_monkey.operation = Operation(*tokens)
// elif "Test: divisible" in line:
//     new_monkey.div_by = extract_all_ints(line).pop()
// elif "If true:" in line:
//     new_monkey.if_true = extract_all_ints(line).pop()
// elif "If false:" in line:
//     new_monkey.if_false = extract_all_ints(line).pop()
//     monkeys.append(new_monkey)

// Monkey 1:
//   Starting items: 54, 65, 75, 74
//   Operation: new = old + 6
//   Test: divisible by 19
//     If true: throw to monkey 2
//     If false: throw to monkey 0

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
fn solve(monkeys: &mut Vec<Monkey>, rounds: usize, part2: bool) -> usize {
    let mod_op: i64 = monkeys.iter().fold(1, |accu, m| accu * m.div_by);
    for _ in 0..rounds {
        for i in 0..monkeys.len() {
            monkeys[i].inspect_cnt += monkeys[i].items.len();
            let mut temp = vec![];
            for item in monkeys[i].items.iter() {
                let mut op2 = item.clone();
                if let Operand::Value(i) = monkeys[i].operation.operand_2 {
                    op2 = i;
                }
                let mut result: i64 = if monkeys[i].operation.operator == '+' {
                    item.clone() + op2
                } else {
                    item.clone() * op2
                };
                result = if part2 { result % mod_op } else { (result / 3) };
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
    monkeys
        .iter()
        .map(|x| x.inspect_cnt)
        .collect::<BinaryHeap<_>>()
        .drain()
        .take(2)
        .into_iter()
        .fold(1, |accu, x| accu * x)
}

fn part1(monkeys: &mut Vec<Monkey>) -> usize {
    solve(monkeys, 20, false)
}

fn part2(monkeys: &mut Vec<Monkey>) -> usize {
    solve(monkeys, 10_000, true)
}

fn main() {
    let input = include_str!("../../../inputs/input_11.txt");
    let mut monkeys = parse(input);
    let mut monkey1 = monkeys.clone();
    println!("{:?}", monkeys);
    println!("Part 1: {}", part1(&mut monkey1));
    println!("Part 2: {}", part2(&mut monkeys));
}
