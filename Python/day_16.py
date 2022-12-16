import sys
from collections import deque
from copy import copy
from dataclasses import dataclass, field
from typing import List, Set

from aoc import *


@dataclass
class Valve:
    name: str = 0
    pressure: int = 0
    connected_to: List = field(default_factory=list)


@dataclass
class State:
    pos: str = 0
    time: int = 0
    pressure: int = 0
    pressure_sum: int = 0
    visited: Set = field(default_factory=set)
    history: Set = field(default_factory=list)


# Valve JJ has flow rate=21; tunnel leads to valve II, AA
def parse_input(lines):
    valves = []
    for line in lines:
        val = Valve()
        val.pressure = extract_all_ints(line)[0]
        tokens = re.split(' |,|=', line)
        val.name = tokens[1]
        val.connected_to = list(filter(len, tokens[10:]))
        valves.append(val)

    return valves


def part_1(valves, time=30):
    valve_dict = {v.name: v for v in valves}
    pressures = {v.name: v.pressure for v in valves}
    open = set()
    dists ={valve.name: find_shortest_paths(valve_dict,valve, valves) for valve in valves}
    print(dists)
    cur_pressure = 0
    sum_pressure = 0
    queue = deque()
    best = 0
    queue.append(State(pos="AA", time=1, pressure=0, pressure_sum=0))
    visited = {}
    while len(queue) > 0:
        cur = queue.popleft()
        if cur.pos not in cur.visited:
            if valve_dict[cur.pos].pressure > 0:
                cur.time += 1
                cur.pressure_sum += cur.pressure
            cur.visited.add(cur.pos)
            cur.pressure += valve_dict[cur.pos].pressure
        costs = [((time - cur.time - abs(dists[cur.pos][val.name]) - 1) * val.pressure, val)
                 for val in filter(lambda v: v.name not in cur.visited and v.pressure > 0, valves)]
       # print(sorted(costs, key=lambda x: x[0], reverse=True))
        for cost in costs:
            travel_time =  dists[cur.pos][cost[1].name]
            if cur.time +travel_time > time:
                continue
            next = State(pos=cost[1].name, time=cur.time +travel_time, pressure=cur.pressure,
                  pressure_sum=cur.pressure_sum+ travel_time * cur.pressure, visited=copy(cur.visited), history=copy(cur.history))
            next.history.append((cur.time +travel_time, cost[1].name, cur.pressure,cur.pressure_sum))
            next.visited
            key = ''.join(sorted(next.visited))
            print(key,next.time )
            if key in visited:
                if visited[key] >= cur.time:
                    queue.append(next)
                    visited[key] = cur.time
            else:
                visited[key] = cur.time
                queue.append(next)


        new = cur.pressure_sum + cur.pressure*(time+1-cur.time)
        if new > best:
            best = new
            print(cur)
    return best


# def find_max(cur_pressure:int, i:int, visited : List[str], max_time=30):
#    ((time - i - abs(dist[val.name] - dist[cur.name]) - 1) * val.pressure, val)
#    for val in filter(lambda v: v.name not in open, valves)

def find_shortest_paths(valve_dict,start, valves):
    dist = {v.name: sys.maxsize for v in valves}
    dist[start.name] = 0
    #prev = {}
    queue = deque()
    in_queue = {start.name}
    queue.append(start.name)
    while len(queue) > 0:
        cur: str = queue.popleft()
        in_queue.remove(cur)
        for n in valve_dict[cur].connected_to:
            t_costs = dist[cur] + 1
            if t_costs < dist[n]:
                dist[n] = t_costs
                #prev[n] = cur
                if n not in in_queue:
                    queue.append(n)
                    in_queue.add(n)
    return dist


def part_2(lines):
    pass


def main():
    lines = get_lines("input_16.txt")
    valves = parse_input(lines)
    print("Part 1:", part_1(valves))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
