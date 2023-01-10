use std::collections::HashMap;

type Binop = fn(i64, i64) -> i64;

#[derive(Debug, Clone, Copy)]
struct Node<'a> {
    name: &'a str,
    value: Option<i64>,
    operator: Option<char>,
    left: Option<&'a str>,
    right: Option<&'a str>,
}

fn add(a: i64, b: i64) -> i64 {
    a + b
}

fn sub(a: i64, b: i64) -> i64 {
    a - b
}

fn div(a: i64, b: i64) -> i64 {
    a / b
}
fn mul(a: i64, b: i64) -> i64 {
    a * b
}

fn get_op(c: char) -> Binop {
    match c {
        '+' => add,
        '-' => sub,
        '/' => div,
        '*' => mul,
        _ => unreachable!(),
    }
}

fn parse_input<'a>(lines: &'a str) -> HashMap<&'a str, Node> {
    let mut node_dict = HashMap::new();
    for line in lines.lines() {
        let mut tokens = line.split(':');
        let name = tokens.next().unwrap();
        let rhs: Vec<_> = tokens
            .next()
            .unwrap()
            .split(' ')
            .filter(|a| !a.is_empty())
            .collect();
        let mut value: Option<i64> = None;
        let mut operator: Option<char> = None;
        let mut left: Option<&'a str> = None;
        let mut right: Option<&'a str> = None;
        if rhs.len() == 1 {
            value = Some(rhs[0].trim().parse().unwrap());
        } else {
            left = Some(rhs[0]);
            operator = Some(rhs[1].chars().next().unwrap());
            right = Some(rhs[2]);
        }
        node_dict.insert(
            name,
            Node {
                name,
                value,
                operator,
                left,
                right,
            },
        );
    }
    node_dict
}

fn calc<'a>(node: Node, nodes: &HashMap<&'a str, Node>) -> i64{
    if let Some(val) = node.value{
        return val;
    }
    get_op(node.operator.unwrap())(calc(nodes[node.left.unwrap()], &nodes), calc(nodes[node.right.unwrap()], &nodes))
}

fn part1<'a>(nodes: &HashMap<&'a str, Node>) -> i64 {
    calc(nodes["root"], nodes)
}

fn part2<'a>(nodes: &HashMap<&'a str, Node>) -> i64 {
    0
}

fn main() {
    let input = include_str!("../../../inputs/input_21.txt");
    let nodes = parse_input(input);
    println!("Part 1: {}", part1(&nodes));
    println!("Part 2: {}", part2(&nodes));
}
