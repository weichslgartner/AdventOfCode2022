import itertools
import sys
from collections import deque
from copy import copy
from dataclasses import dataclass, field
from typing import List, Set

from aoc import *

max_pressure = 0
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
    #   in_movement: Set = field(default_factory=set)
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


def part_1(valves, allowed_set,time=25):
    valve_dict = {v.name: v for v in valves}
    dists = {valve.name: find_shortest_paths(valve_dict, valve, valves) for valve in valves}
    print(dists)
    queue = deque()
    best = 0
    queue.append(State(pos="AA", time=0, pressure=0, pressure_sum=0))
    visited = {}
    while len(queue) > 0:
        cur = queue.popleft()
        open_valve(cur_state=cur, valve_dict=valve_dict)
        costs = [((time - cur.time - abs(dists[cur.pos][val.name]) - 1) * val.pressure, val)
                 for val in filter(lambda v: v.name not in cur.visited and v.name in allowed_set and v.pressure > 0, valves)]
        # print(sorted(costs, key=lambda x: x[0], reverse=True))
        for cost in costs:
            travel_time = dists[cur.pos][cost[1].name]
            if cur.time + travel_time > time:
                continue

            next = get_next_state(cur, cost[1].name,travel_time)
            next.pressure_sum += cur.pressure * travel_time
            key = ''.join(sorted(next.visited))
            # print(key,next.time )
            if key in visited:
                if visited[key] >= cur.time:
                    queue.append(next)
                    visited[key] = cur.time
            else:
                visited[key] = cur.time
            queue.append(next)

        new = cur.pressure_sum + cur.pressure * (time + 1 - cur.time)
        if new > best:
            best = new
            print(cur)
    return best


# def find_max(cur_pressure:int, i:int, visited : List[str], max_time=30):
#    ((time - i - abs(dist[val.name] - dist[cur.name]) - 1) * val.pressure, val)
#    for val in filter(lambda v: v.name not in open, valves)

def find_shortest_paths(valve_dict, start, valves):
    dist = {v.name: sys.maxsize for v in valves}
    dist[start.name] = 0
    # prev = {}
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
                # prev[n] = cur
                if n not in in_queue:
                    queue.append(n)
                    in_queue.add(n)
    return dist


def part_2(valves, time=25):
    global max_pressure
    valve_dict = {v.name: v for v in valves}
    max_pressure = sum( v.pressure for v in valves)
    max_pressure_ov = time*max_pressure
    print(max_pressure_ov,max_pressure/time)
    print([v.pressure for v in valves if v.pressure > 0])
    dists = {valve.name: find_shortest_paths(valve_dict, valve, valves) for valve in valves}
    queue = deque()
    best = 0
    queue.append(
        (State(pos="AA", time=1, pressure=0, pressure_sum=0), State(pos="AA", time=1, pressure=0, pressure_sum=0)))
    visited = {}
    while len(queue) > 0:
        me, elephant = queue.popleft()
#        assert (elephant.pressure_sum < max_pressure)
        elephant_old = copy(elephant)
        new_elephant = False
        new_me = False
        # cur_time = None
        if me.time < elephant.time:
            cur_time = me.time
            open_valve(me, valve_dict)
            assert(elephant.pressure_sum == elephant_old.pressure_sum)
            new_me = True
        elif me.time > elephant.time:
            cur_time = elephant.time
            open_valve(elephant, valve_dict)
            new_elephant = True
        else:
            open_valve(elephant, valve_dict)
            open_valve(me, valve_dict)
            assert (elephant.time == me.time)
            cur_time = elephant.time
            new_elephant = True
            new_me = True
        elephant_coice = list(
            filter(lambda v: v.name not in me.visited and v.pressure > 0 and v.name not in elephant.visited,
                   valves)) if new_elephant else [elephant]
        me_choice = list(
            filter(lambda v: v.name not in me.visited and v.pressure > 0 and v.name not in elephant.visited,
                   valves)) if new_me else [me]
        for next_elephant in elephant_coice:
            for next_me in me_choice:
                if (time -cur_time) * max_pressure < best:
                    continue

                if new_me:
                    travel_time = dists[me.pos][next_me.name]
                    if cur_time + travel_time > time:
                        continue
                    next_me_state = get_next_state(me, next_me.name, travel_time)
                else:
                    next_me_state = copy(me)
                if new_elephant:
                    travel_time = dists[elephant.pos][next_elephant.name]
                    if cur_time + travel_time > time:
                        continue
                    next_elephant_state = get_next_state(elephant, next_elephant.name, travel_time)
                 #   assert (next_elephant_state.pressure_sum < max_pressure)

                else:
                    next_elephant_state = copy(elephant)
#                    assert (next_elephant_state.pressure_sum < max_pressure)

                if next_elephant_state.pos == next_me_state.pos:
                    continue
                time_until_next = min(next_me_state.time - cur_time, next_elephant_state.time - cur_time)
                #if time_until_next > 25:
                #    print("debug")
 #               assert (time_until_next >= 0)
#                assert(cur_time + time_until_next <=time )
                #            next.pressure_sum += cur.pressure * travel_time
                before = next_elephant_state.pressure_sum
#                assert( next_elephant_state.pressure_sum < max_pressure)

                next_elephant_state.pressure_sum += elephant.pressure * time_until_next
              #  if next_elephant_state.pressure_sum > max_pressure:

              #      print(elephant)
                next_me_state.pressure_sum += me.pressure * time_until_next

                key = ''.join(sorted(next_me_state.visited | next_elephant_state.visited))
                # print(key,next.time )
                if key in visited:
                    if visited[key] >= me.time:
                        queue.append((next_me_state, next_elephant_state))
                        visited[key] = me.time
                else:
                    visited[key] = me.time
                queue.append((next_me_state, next_elephant_state))

        #new = me.pressure_sum + me.pressure * (time + 1 - me.time) + elephant.pressure_sum + elephant.pressure * (time + 1 - elephant.time)
        s = calc_pressure(elephant, me, time, valve_dict)
        if s > best:
            best = s
            print(s, best, me.pressure, elephant.pressure, me, elephant)

    return best


def calc_pressure(elephant, me, time, valve_dict):
    s = 0
    for state in me.history:
        v_time, pos = state[0], state[1]
        s += (time - v_time) * valve_dict[pos].pressure
    for state in elephant.history:
        v_time, pos = state[0], state[1]
        s += (time - v_time) * valve_dict[pos].pressure
    return s


def get_next_state(cur, next_me_name, travel_time):
    next = State(pos=next_me_name, time=cur.time + travel_time + 1, pressure=cur.pressure,
                 pressure_sum=copy(cur.pressure_sum), visited=copy(cur.visited),
                 history=copy(cur.history)
                 )
    next.history.append((cur.time + travel_time, next_me_name, cur.pressure, cur.pressure_sum))
    return next



def open_valve(cur_state, valve_dict):
    global max_pressure
    if cur_state.pos not in cur_state.visited:
        if valve_dict[cur_state.pos].pressure > 0:
            # if cur_state.pressure > 0:
#            assert (cur_state.pressure_sum < max_pressure)

            cur_state.pressure_sum += cur_state.pressure
#            assert (cur_state.pressure_sum < max_pressure)
        cur_state.visited.add(cur_state.pos)
        cur_state.pressure += valve_dict[cur_state.pos].pressure
    return valve_dict[cur_state.pos].pressure


def open_to_pressure(visited, valve_dict):
    return sum(valve_dict[v].pressure for v in visited)


def main():
    lines = get_lines("input_16.txt")
    valves = parse_input(lines)
    press_valves = set(valve.name for valve in valves if valve.pressure >0)
    best = 0
    for i in range(len(press_valves)//2 +1 ):
        combis = itertools.combinations(press_valves,i)
        for c in combis:
           # print(c)
            me = part_1(valves, allowed_set=set(c),time=25)
            elephant = part_1(valves, allowed_set=press_valves-set(c), time=25)
            if me + elephant > best:
                best = me + elephant
                #print("new best",best,press_valves,elephant_set )

    press_valves = set(valve.name for valve in valves if valve.pressure >0)
    press_valves.add("AA")
    print("Part 1:", part_1(valves, allowed_set=set(press_valves), time=29))
    print("Part 2:", best)  # too hi 2712 too low 2068
#incorrect 2175

if __name__ == '__main__':
    main()
