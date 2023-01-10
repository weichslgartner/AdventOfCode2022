use std::collections::HashMap;

const HUMN: &str = "humn";

#[derive(Debug, Clone, Copy)]
struct Node<'a> {
    name: &'a str,
    value: Option<i64>,
    operator: Option<char>,
    left: Option<&'a str>,
    right: Option<&'a str>,
}

impl<'a> Node<'a> {
    fn new(name: &'a str) -> Self {
        Node {
            name,
            value: None,
            operator: None,
            left: None,
            right: None,
        }
    }
}

fn op_norm(c: char, a: i64, b: i64) -> i64 {
    match c {
        '+' => a + b,
        '-' => a - b,
        '/' => a / b,
        '*' => a * b,
        _ => unreachable!(),
    }
}

fn op_inv_left(c: char, a: i64, b: i64) -> i64 {
    match c {
        '+' => a - b,
        '-' => a + b,
        '/' => a * b,
        '*' => a / b,
        '=' => a + b, // special case for root node
        _ => unreachable!(),
    }
}

fn op_inv_right(c: char, a: i64, b: i64) -> i64 {
    match c {
        '+' => a - b,
        '-' => b - a,
        '/' => b / a,
        '*' => a / b,
        _ => unreachable!(),
    }
}

fn parse_input(lines: &str) -> HashMap<&str, Node> {
    let mut node_dict = HashMap::new();
    for line in lines.lines() {
        let mut tokens = line.split(':');
        let mut node = Node::new(tokens.next().unwrap());
        let rhs: Vec<_> = tokens
            .next()
            .unwrap()
            .split(' ')
            .filter(|a| !a.is_empty())
            .collect();
        if rhs.len() == 1 {
            node.value = Some(rhs[0].trim().parse().unwrap());
        } else {
            node.left = Some(rhs[0]);
            node.operator = Some(rhs[1].chars().next().unwrap());
            node.right = Some(rhs[2]);
        }
        node_dict.insert(node.name, node);
    }
    node_dict
}

fn calc(node: Node, nodes: &HashMap<&str, Node>) -> i64 {
    if let Some(val) = node.value {
        return val;
    }
    op_norm(
        node.operator.unwrap(),
        calc(nodes[node.left.unwrap()], nodes),
        calc(nodes[node.right.unwrap()], nodes),
    )
}

fn tree_contains(node: Option<Node>, name: &str, nodes: &HashMap<&str, Node>) -> bool {
    if let Some(node) = node {
        if node.value.is_some() {
            return node.name == name;
        }
        return tree_contains(nodes.get(&node.left.unwrap()).copied(), name, nodes)
            || tree_contains(nodes.get(&node.right.unwrap()).copied(), name, nodes);
    }
    false
}

fn solve(node: Node, target: i64, nodes: &HashMap<&str, Node>) -> i64 {
    if let Some(name) = node.left {
        if name == HUMN {
            return op_inv_left(
                node.operator.unwrap(),
                target,
                calc(nodes[node.right.unwrap()], nodes),
            );
        }
    }
    if let Some(name) = node.right {
        if name == HUMN {
            return op_inv_right(
                node.operator.unwrap(),
                target,
                calc(nodes[node.left.unwrap()], nodes),
            );
        }
    }
    if tree_contains(nodes.get(node.left.unwrap()).copied(), HUMN, nodes) {
        let res = calc(nodes[&node.right.unwrap()], nodes);
        let target = op_inv_left(node.operator.unwrap(), target, res);
        return solve(nodes[node.left.unwrap()], target, nodes);
    }
    let res = calc(nodes[&node.left.unwrap()], nodes);
    let target = op_inv_right(node.operator.unwrap(), target, res);
    solve(nodes[node.right.unwrap()], target, nodes)
}

fn part1(nodes: &HashMap<&str, Node>) -> i64 {
    calc(nodes["root"], nodes)
}

fn part2(nodes: &HashMap<&str, Node>) -> i64 {
    solve(nodes["root"], 0, nodes)
}

fn main() {
    let input = include_str!("../../../inputs/input_21.txt");
    let mut nodes = parse_input(input);
    println!("Part 1: {}", part1(&nodes));
    nodes
        .entry("root")
        .and_modify(|node| node.operator = Some('='));
    println!("Part 2: {}", part2(&nodes));
}
