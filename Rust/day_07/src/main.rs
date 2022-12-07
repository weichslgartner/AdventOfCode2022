use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

const TOTAL_SIZE: usize = 70000000;

const SIZE_NEEDED: usize = 30000000;

#[derive(PartialEq)]
struct Node {
    pub name: String,
    pub size: Option<usize>,
    pub is_file: Option<bool>,
    pub children: HashMap<String, Rc<RefCell<Node>>>,
    pub parent: Option<Rc<RefCell<Node>>>,
}

impl Node {
    pub fn new(name: String) -> Node {
        Node {
            name,
            size: None,
            is_file: Some(false),
            children: HashMap::new(),
            parent: None,
        }
    }
}

fn parse_input(lines: &str) -> Rc<RefCell<Node>> {
    let root = Rc::new(RefCell::new(Node::new("/".to_string())));
    let mut cur_node = Rc::clone(&root);
    for line in lines.lines() {
        let tokenz: Vec<&str> = line.split(' ').collect();
        if line.starts_with('$') {
            if line.contains("cd") {
                let folder = tokenz[2];
                if folder == ".." {
                    let next = Rc::clone(cur_node.borrow().parent.as_ref().unwrap());
                    cur_node = next;
                } else if folder == "/" {
                    cur_node = root.clone();
                } else {
                    let next = cur_node.borrow_mut().children.get(folder).unwrap().clone();
                    cur_node = next;
                }
            }
        } else if let [size_or_dir, name] = &tokenz[..] {
            if *size_or_dir == "dir" {
                if !cur_node.borrow().children.contains_key(*name) {
                    let child = Rc::new(RefCell::new(Node::new(name.to_string())));
                    let mut mut_child = child.borrow_mut();
                    mut_child.parent = Some(Rc::clone(&cur_node));
                    cur_node
                        .borrow_mut()
                        .children
                        .insert(name.to_string(), Rc::clone(&child));
                }
            } else if !cur_node.borrow().children.contains_key(*name) {
                let child = Rc::new(RefCell::new(Node::new(name.to_string())));
                let mut mut_child = child.borrow_mut();
                mut_child.is_file = Some(true);
                mut_child.size = Some(size_or_dir.parse().unwrap());
                mut_child.parent = Some(Rc::clone(&cur_node));
                cur_node
                    .borrow_mut()
                    .children
                    .insert(name.to_string(), Rc::clone(&child));
            }
        }
    }
    root
}

fn calc_sum(node: Rc<RefCell<Node>>, sizes: &mut Vec<usize>) -> usize {
    if node.borrow().is_file.unwrap() {
        return node.borrow().size.unwrap();
    }
    let mut sum_c = 0;
    for child in node.borrow().children.values() {
        sum_c += calc_sum(Rc::clone(&child), sizes);
    }
    sizes.push(sum_c);
    sum_c
}

fn part1(input: &str) -> usize {
    let root = parse_input(input);
    let mut sizes = vec![];
    calc_sum(root, &mut sizes);
    sizes.iter().filter(|x| **x < 100000).sum()
}

fn part2(input: &str) -> usize {
    let root = parse_input(input);
    let mut sizes = vec![];
    let cur_used = calc_sum(root, &mut sizes);
    let needed = SIZE_NEEDED - (TOTAL_SIZE - cur_used);
    *sizes.iter().filter(|x| **x > needed).min().unwrap()
}

fn main() {
    let input = include_str!("../../../inputs/input_07.txt");
    println!("Part 1: {}", part1(input));
    println!("Part 2: {}", part2(input));
}
