import sys
from collections import deque, defaultdict, namedtuple
from copy import copy, deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict, List

from aoc import get_lines, extract_all_ints


class Material(Enum):
    ORE = 0  # "ore"
    CLAY = 1  # "clay"
    OBSIDIAN = 2  # "obsidian"
    GEODE = 3  # "geode"


@dataclass
class Robot:
    type: Material
    costs: Tuple


@dataclass
class State:
    time: int
    robots: Dict
    resources: Dict


def state_to_str(state: State):
    res = ""
    for material in Material:
        res += f"{state.robots[material]}-{state.resources[material]}-"
    return res


class Costs(namedtuple('Costs', 'costs material')):
    pass

def triangular(n):
    return int(n * (n + 1) / 2)

def parse_input(lines):
    blueprints = {}
    for line in lines:
        tokens = line.strip().split('.')
        bid = None
        for i, token in enumerate(tokens):
            if i == 0:
                ints = extract_all_ints(token)
                bid = ints[0]
                blueprints[bid] = {}
                blueprints[bid][Material.ORE] = Robot(type=Material.ORE,
                                                      costs=[Costs(costs=ints[1], material=Material.ORE)])
            elif i == 1:
                ints = extract_all_ints(token)
                blueprints[bid][Material.CLAY] = Robot(type=Material.CLAY, costs=[Costs(ints[0], Material.ORE)])
            elif i == 2:
                ints = extract_all_ints(token)
                blueprints[bid][Material.OBSIDIAN] = Robot(type=Material.OBSIDIAN, costs=[Costs(ints[0], Material.ORE),
                                                                                          Costs(ints[1],
                                                                                                Material.CLAY)])
            elif i == 3:
                ints = extract_all_ints(token)
                blueprints[bid][Material.GEODE] = Robot(type=Material.GEODE, costs=[Costs(ints[0], Material.ORE),
                                                                                    Costs(ints[1], Material.OBSIDIAN)])
    print(blueprints)
    # Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
    return blueprints


def part_1(blueprints):
    sum = 0
    for k, b in list(blueprints.items()):
        print(k, b)
        res = optimize_blueprint(b)
        sum += k * res

    return sum


def optimize_blueprint(blueprint, max_time=24):
    queue = deque()
    start = State(time=1, robots=defaultdict(int, {Material.ORE: 1}), resources=defaultdict(int))
    queue.append(start)
    max_geodes = 0
    max_iter = 300_000_000
    i = 0
    visited = defaultdict(lambda: sys.maxsize)
    while len(queue) > 0:
        i += 1
        if i > max_iter:
            break
        cur = queue.pop()
        key = state_to_str(cur)
        if visited[key] <= cur.time:
            continue
        visited[key] = cur.time
        assert (cur.time <= max_time)
        for robot, n in cur.robots.items():
            cur.resources[robot] += n
       # if triangular(max_time - cur.time) <= max_geodes:
       #     continue
        if cur.time == max_time:
            if cur.resources[Material.GEODE] > max_geodes:
                max_geodes = cur.resources[Material.GEODE]
                print(max_geodes, cur)
        else:
            if cur.resources[Material.GEODE] + triangular(((max_time - cur.time) +2))  < max_geodes :
               # print("ignore",max_geodes,cur)
                continue
            cur.time += 1



            if can_build(cur, blueprint[Material.GEODE]):
                queue.append(build_robot(blueprint, cur, Material.GEODE))
            else:
                queue.append(cur)
                for new_robot in [Material.OBSIDIAN, Material.CLAY, Material.ORE]:
                    cbuild = can_build(cur, blueprint[new_robot])
                    if cbuild:
                        next = build_robot(blueprint, cur, new_robot)
                        queue.append(next)
    return max_geodes


def build_robot(blueprint, cur, new_robot_type):
    new_robots = deepcopy(cur.robots)
    new_robots[new_robot_type] += 1
    new_resource = deepcopy(cur.resources)
    # if new_robot.type == Material.GEODE:
    #    print("debug")
    for to_substract in blueprint[new_robot_type].costs:
        new_resource[to_substract.material] -= to_substract.costs
    return State(time=cur.time, robots=new_robots, resources=new_resource)


def can_build(cur, robot):
    cbuild = True
    for build_cost in robot.costs:
        if cur.resources[build_cost.material] < build_cost.costs + cur.robots[build_cost.material]:
            cbuild = False
            break
    return cbuild


def part_2(blueprints):
    sum = 1
    for k, b in list(blueprints.items())[:3]:
        print(k, b)
        res = optimize_blueprint(b,32)
        sum *= res

    return sum


def main():
    lines = get_lines("input_19.txt") #1009 too low 1045 too low
    blueprints = parse_input(lines)
    print("Part 1:", part_1(blueprints))
    # part2 still doesn't produce correct result; solution in rust
    print("Part 2:", part_2(blueprints))


if __name__ == '__main__':
    main()
