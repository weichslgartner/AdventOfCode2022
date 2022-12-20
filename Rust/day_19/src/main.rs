use futures::join;
use rayon::prelude::*;
use std::{
    collections::{HashMap},
    hash::Hash,
    hash::Hasher,
};

use int_enum::IntEnum;
use lazy_static::lazy_static;
use regex::Regex;


#[repr(u8)]
#[derive(Clone, Copy, Debug, Eq, PartialEq, IntEnum)]
pub enum Material {
    ORE = 0,
    CLAY = 1,
    OBSIDIAN = 2,
    GEODE = 3,
}

type Costs = [u8; 4];
type Blueprint = [Costs; 4];

#[derive(Clone, Copy, Debug)]
struct State {
    time: u8,
    robots: Costs,
    resources: Costs,
}

impl Hash for State {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.robots.hash(state);
        self.resources.hash(state);
    }
}
impl PartialEq for State {
    fn eq(&self, other: &Self) -> bool {
        self.robots == other.robots && self.resources == other.resources
    }
}
impl Eq for State {}

fn parse(input: &str) -> Vec<Blueprint> {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"-?\d+").unwrap();
    }
    input
        .lines()
        .map(|line| {
            RE.find_iter(line)
                .filter_map(|digits| digits.as_str().parse::<u8>().ok())
                .collect::<Vec<_>>()
        })
        .map(|tokenz| {
            let mut bluepr: Blueprint = [[0; 4]; 4];

            bluepr[Material::ORE.int_value() as usize][Material::ORE.int_value() as usize] =
                tokenz[1];
            bluepr[Material::CLAY.int_value() as usize][Material::ORE.int_value() as usize] =
                tokenz[2];
            bluepr[Material::OBSIDIAN.int_value() as usize][Material::ORE.int_value() as usize] =
                tokenz[3];
            bluepr[Material::OBSIDIAN.int_value() as usize][Material::CLAY.int_value() as usize] =
                tokenz[4];
            bluepr[Material::GEODE.int_value() as usize][Material::ORE.int_value() as usize] =
                tokenz[5];
            bluepr[Material::GEODE.int_value() as usize][Material::OBSIDIAN.int_value() as usize] =
                tokenz[6];

            bluepr
        })
        .collect::<Vec<_>>()
}

fn triangular(n: u32) -> u32 {
    n * (n + 1) / 2
}

fn optimize_blueprint(blueprint: &Blueprint, maxtime: u8) -> usize {
    let mut queue: Vec<State> = Vec::new();
    let mut visited: HashMap<State, u8> = HashMap::new();
    let mut best = 0;
    queue.push(State {
        time: 0,
        robots: [1, 0, 0, 0],
        resources: [0; 4],
    });

    while !queue.is_empty() {
        let mut cur = queue.pop().unwrap();
        if visited.contains_key(&cur) && visited.get(&cur).unwrap() <= &cur.time {
            continue;
        }
        visited.insert(cur, cur.time);
        let build_candidates: Vec<_> = (0..4)
            .map(|i| (i, can_build(cur, blueprint[i])))
            .filter(|(_,x)| *x)
            .map(|(material,_)| Material::from_int(material as u8).unwrap())
            .collect();
        harvest(&mut cur);
        cur.time += 1;
        if cur.time == maxtime {
            if cur.resources[Material::GEODE.int_value() as usize] > best {
                best = cur.resources[Material::GEODE.int_value() as usize];
            }
            continue;
        }
        if cur.resources[Material::GEODE.int_value() as usize] as u32
            + triangular((maxtime - cur.time) as u32 + 2)
            < best as u32
        {
            continue;
        }

        if build_candidates.contains(&Material::GEODE) {
            let mut next_state = cur;
            spend(
                &mut next_state,
                blueprint[Material::GEODE.int_value() as usize],
            );
            build(&mut next_state, Material::GEODE);

            queue.push(next_state);
        } else {
            queue.push(cur);
            for candidate in build_candidates {
                let mut next_state = cur;
                spend(&mut next_state, blueprint[candidate.int_value() as usize]);
                build(&mut next_state, candidate);
                queue.push(next_state);
            }
        }
    }
    best.into()
}

fn harvest(state: &mut State) {
    for (i, robot) in state.robots.iter().enumerate() {
        state.resources[i] += robot;
    }
}

fn spend(state: &mut State, costs: Costs) {
    for (i, cost) in costs.iter().enumerate() {
        state.resources[i] -= cost;
    }
}

fn build(state: &mut State, material: Material) {
    state.robots[material.int_value() as usize] += 1;
}

fn can_build(state: State, costs: Costs) -> bool {
    for (i, cost) in costs.iter().enumerate() {
        if state.resources[i] < *cost {
            return false;
        }
    }
    true
}

async fn part1(blueprints: &Vec<Blueprint>) -> usize {
    blueprints
        .par_iter()
        .enumerate()
        .map(|(i, blueprint)| (i + 1) * optimize_blueprint(blueprint, 24))
        .sum()
}

async fn part2(blueprints: &Vec<Blueprint>) -> usize {
    blueprints
        .par_iter()
        .take(3)
        .map(|blueprint| optimize_blueprint(blueprint, 32))
        .product()
}

async fn async_main() {
    let input = include_str!("../../../inputs/input_19.txt");
    let blueprints = parse(input);
    let res1 = part1(&blueprints);
    let res2 = part2(&blueprints);
    let (p1, p2) = join!(res1, res2);
    println!("Part 1: {p1}");
    println!("Part 2: {p2}");
}

#[tokio::main]
async fn main() {
    async_main().await;
}
