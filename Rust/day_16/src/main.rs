use bit_set::BitSet;
use itertools::Itertools;
use rayon::prelude::*;
use std::collections::{HashMap, HashSet, VecDeque};

#[derive(Clone, Debug, Eq, PartialEq)]
struct Valve {
    name: String,
    pressure: u32,
    connected_to: Vec<String>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct State<'a> {
    pos: &'a str,
    time: u8,
    pressure: u32,
    pressure_sum: u32,
    visited: BitSet,
}

fn parse(input: &str) -> HashMap<String, Valve> {
    input
        .lines()
        .map(|line| {
            line.split(|c| c == ' ' || c == ',' || c == '=' || c == ';')
                .collect()
        })
        .map(|tokenz: Vec<_>| Valve {
            name: tokenz[1].to_owned(),
            pressure: tokenz[5].parse().unwrap(),
            connected_to: tokenz[11..]
                .iter()
                .map(|x| x.to_string())
                .filter(|x| !x.is_empty())
                .collect(),
        })
        .map(|v| (v.name.clone(), v))
        .collect()
}

fn find_shortest_paths<'a>(
    start: &'a String,
    valves: &'a HashMap<String, Valve>,
) -> HashMap<&'a str, u8> {
    let mut dist: HashMap<&'a str, u8> = valves
        .values()
        .map(|v| (v.name.as_ref(), std::u8::MAX))
        .collect();
    dist.insert(start.as_str(), 0);

    let mut queue: VecDeque<String> = VecDeque::new();
    let mut in_queue = HashSet::new();
    in_queue.insert(start.to_owned());
    queue.push_back(start.to_owned());
    while !queue.is_empty() {
        let cur = queue.pop_front().unwrap();
        in_queue.remove(&cur);
        for n in valves[&cur].connected_to.iter() {
            let t_costs = dist[&*cur] + 1;
            if t_costs < *dist.get::<&str>(&n.as_str()).unwrap() {
                dist.insert(n.as_ref(), t_costs);
                if !in_queue.contains(n) {
                    queue.push_back(n.to_owned());
                    in_queue.insert(n.to_owned());
                }
            }
        }
    }
    dist
}

fn part1(
    valves: &HashMap<String, Valve>,
    dists: &HashMap<&str, HashMap<&str, u8>>,
    allowed_valves: BitSet,
    time: u8,
) -> u32 {
    let mut queue: VecDeque<State> = VecDeque::new();
    let mut mem: HashMap<BitSet, u8> = HashMap::new();
    let start_state = State {
        pos: "AA",
        time: 0,
        pressure: 0,
        pressure_sum: 0,
        visited: BitSet::with_capacity(valves.len()),
    };
    let mut best: u32 = 0;
    queue.push_back(start_state);
    while !queue.is_empty() {
        let cur = queue.pop_back().unwrap();
        let costs = cur.pressure_sum + cur.pressure * ((time + 1 - cur.time) as u32);
        if cur.time <= time && costs > best {
            best = costs;
        }
        for (next_pos, cost) in dists[&cur.pos].iter().filter(|(x, t)| {
            cur.time + **t < time
                && !cur.visited.contains(valve2usize(x))
                && allowed_valves.contains(valve2usize(x))
        }) {
            let mut new_visited = cur.visited.clone();
            new_visited.insert(valve2usize(next_pos));
            if !mem.contains_key(&new_visited) || mem[&new_visited] >= cur.time - 2 + *cost {
                mem.insert(new_visited.clone(), cur.time + *cost + 1);
                queue.push_back(State {
                    pos: next_pos,
                    time: cur.time + *cost + 1,
                    pressure: cur.pressure + valves[*next_pos].pressure,
                    pressure_sum: cur.pressure_sum + cur.pressure * ((*cost + 1) as u32),
                    visited: new_visited,
                });
            }
        }
    }
    best
}

fn part2(
    valves: &HashMap<String, Valve>,
    dists: &HashMap<&str, HashMap<&str, u8>>,
    time: u8,
) -> u32 {
    let press_valves: BitSet = valves
        .iter()
        .filter(|(_, v)| v.pressure > 0)
        .map(|(key, _)| valve2usize(key.as_str()))
        .collect();
    
    (0..=press_valves.len() / 2).into_par_iter().map(|i| {
        let it = press_valves.iter().combinations(i);
        let mut best = 0;
        for c in it {
            let me_set: BitSet = c.iter().copied().collect();
            let elephant_set: BitSet = press_valves.difference(&me_set).collect();
            let me = part1(valves, dists, me_set, time);
            let elephant = part1(valves, dists, elephant_set, time);
            if me + elephant > best {
                best = me + elephant;
            }
        }
        best
    }).max().unwrap()
}

fn valve2usize(input: &str) -> usize {
    assert!(input.len() == 2);
    (input.chars().next().unwrap() as usize - 'A' as usize) * 32
        + (input.chars().nth(1).unwrap() as usize - 'A' as usize)
}

fn main() {
    let input = include_str!("../../../inputs/input_16.txt");
    let valves = parse(input);
    let dists: HashMap<&str, HashMap<&str, u8>> = valves
        .keys()
        .map(|name| (name.as_str(), find_shortest_paths(name, &valves)))
        .collect();
    //println!("{:?} {}", valves.keys().into_iter().map(|x| valve2usize(x.as_str())).collect::<Vec<_>>(), valves.len());
    println!(
        "Part 1: {}",
        part1(
            &valves,
            &dists,
            valves
                .iter()
                .filter(|(_, valve)| valve.pressure > 0)
                .map(|(key, _)| valve2usize(key.as_str()))
                .collect(),
            29
        )
    );
    println!("Part 2: {}", part2(&valves, &dists, 25));
}
