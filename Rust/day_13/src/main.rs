use std::{cmp::Ordering, collections::VecDeque};

#[derive(Debug, Clone, Eq, PartialEq)]
enum Packet {
    Integer(i32),
    List(Vec<Packet>),
}

impl PartialOrd<Self> for Packet {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Packet {
    fn cmp(&self, other: &Self) -> Ordering {
        match (self, other) {
            (Packet::Integer(l), Packet::Integer(r)) => l.cmp(r),
            (Packet::Integer(l), Packet::List(_)) => {
                Packet::List(vec![Packet::Integer(*l)]).cmp(other)
            }
            (Packet::List(_), Packet::Integer(r)) => {
                self.cmp(&Packet::List(vec![Packet::Integer(*r)]))
            }
            (Packet::List(ls), Packet::List(rs)) => {
                for (l, r) in ls.iter().zip(rs) {
                    match l.cmp(r) {
                        Ordering::Less => return Ordering::Less,
                        Ordering::Greater => return Ordering::Greater,
                        Ordering::Equal => {}
                    }
                }
                ls.len().cmp(&rs.len())
            }
        }
    }
}

fn tokenize(input: &str) -> VecDeque<String> {
    let mut tokens = VecDeque::new();
    let mut number = String::from("");

    for c in input.chars() {
        match c {
            '[' => {
                tokens.push_back(String::from("["));
            }
            ',' => {
                if !number.is_empty() {
                    tokens.push_back(number.clone());
                    number = String::from("");
                }
            }
            ']' => {
                if !number.is_empty() {
                    tokens.push_back(number.clone());
                    number = String::from("");
                }
                tokens.push_back(String::from("]"));
            }
            _ => number.push(c),
        }
    }
    tokens.pop_front();
    tokens.pop_back();
    tokens
}

fn parse_packet(tokens: &mut VecDeque<String>) -> Packet {
    let mut v = vec![];
    while let Some(token) = tokens.pop_front() {
        match token.as_str() {
            "[" => v.push(parse_packet(tokens)),
            "]" => break,
            x => v.push(Packet::Integer(x.parse().unwrap())),
        }
    }
    Packet::List(v)
}

fn parse(input: &str) -> Vec<Vec<Packet>> {
    input
        .split("\n\n")
        .map(|pair| {
            pair.lines()
                .map(tokenize)
                .map(|mut tokens| parse_packet(&mut tokens))
                .collect()
        })
        .collect()
}

fn part1(pairs: &[Vec<Packet>]) -> usize {
    pairs
        .iter()
        .enumerate()
        .map(|(i, x)| (i + 1, x[0] < x[1]))
        .filter(|(_, x)| *x)
        .map(|(i, _)| i)
        .sum()
}

fn part2(pairs: Vec<Vec<Packet>>, divider_packets: Vec<Packet>) -> usize {
    let mut packets: Vec<Packet> = pairs.into_iter().flatten().collect();
    divider_packets.iter().for_each(|p| packets.push(p.clone()));
    packets.sort();
    packets
        .iter()
        .enumerate()
        .filter(|(_, packet)| divider_packets.contains(packet))
        .map(|(i, _)| i + 1)
        .product()
}

fn main() {
    let input = include_str!("../../../inputs/input_13.txt");
    let pairs = parse(input);
    let divider = parse("[[2]]\n[[6]]").into_iter().flatten().collect();
    println!("Part 1: {}", part1(&pairs));
    println!("Part 2: {}", part2(pairs, divider));
}
