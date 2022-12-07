use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

const TOTAL_SIZE: usize = 70000000;

const SIZE_NEEDED: usize = 30000000;

struct Node {
    pub size: Option<usize>,
    pub is_file: Option<bool>,
    pub children: HashMap<String, Rc<RefCell<Node>>>,
    pub parent: Option<Rc<RefCell<Node>>>,
}

impl Node {
    pub fn new() -> Node {
        Node {
            size: None,
            is_file: Some(false),
            children: HashMap::new(),
            parent: None,
        }
    }
}

fn parse_input(lines: &str) -> Rc<RefCell<Node>> {
    let root = Rc::new(RefCell::new(Node::new()));
    let mut cur_node = Rc::clone(&root);
    for line in lines.lines() {
        let tokenz: Vec<&str> = line.split(' ').collect();
        if line.starts_with('$') {
            cur_node = parse_command(line, &tokenz, &cur_node, &root);
        } else if let [size_or_dir, name] = &tokenz[..] {
            parse_ls_output(size_or_dir, &cur_node, name);
        }
    }
    root
}

fn parse_ls_output(size_or_dir: &&str, cur_node: &Rc<RefCell<Node>>, name: &&str) {
    if *size_or_dir == "dir" && !cur_node.borrow().children.contains_key(*name) {
        let child = Rc::new(RefCell::new(Node::new()));
        let mut mut_child = child.borrow_mut();
        mut_child.parent = Some(Rc::clone(cur_node));
        cur_node
            .borrow_mut()
            .children
            .insert(name.to_string(), Rc::clone(&child));
    } else if !cur_node.borrow().children.contains_key(*name) {
        let child = Rc::new(RefCell::new(Node::new()));
        let mut mut_child = child.borrow_mut();
        mut_child.is_file = Some(true);
        mut_child.size = Some(size_or_dir.parse().unwrap());
        mut_child.parent = Some(Rc::clone(cur_node));
        cur_node
            .borrow_mut()
            .children
            .insert(name.to_string(), Rc::clone(&child));
    }
}

fn parse_command(
    line: &str,
    tokenz: &[&str],
    cur_node: &Rc<RefCell<Node>>,
    root: &Rc<RefCell<Node>>,
) -> Rc<RefCell<Node>> {
    if !line.contains("cd") {
        return cur_node.clone();
    }
    let folder = tokenz[2];
    match folder {
        ".." => Rc::clone(cur_node.borrow().parent.as_ref().unwrap()),
        "/" => root.clone(),
        _ => cur_node.borrow().children.get(folder).unwrap().clone(),
    }
}

fn calc_sum(node: &Rc<RefCell<Node>>, sizes: &mut Vec<usize>) -> usize {
    if node.borrow().is_file.unwrap() {
        return node.borrow().size.unwrap();
    }
    let mut sum_c = 0;
    for child in node.borrow().children.values() {
        sum_c += calc_sum(&Rc::clone(child), sizes);
    }
    sizes.push(sum_c);
    sum_c
}

fn part1(sizes: &[usize]) -> usize {
    sizes.iter().filter(|x| **x < 100000).sum()
}

fn part2(sizes: &[usize], cur_used: usize) -> usize {
    let needed = SIZE_NEEDED - (TOTAL_SIZE - cur_used);
    *sizes.iter().filter(|x| **x > needed).min().unwrap()
}

fn main() {
    let input = include_str!("../../../inputs/input_07.txt");
    let root = parse_input(input);
    let mut sizes = vec![];
    let cur_used = calc_sum(&root, &mut sizes);
    println!("Part 1: {}", part1(&sizes));
    println!("Part 2: {}", part2(&sizes, cur_used));
}
