import copy
import heapq
from dataclasses import dataclass, field
from functools import reduce
from operator import add
from typing import List

from aoc import get_lines, extract_all_ints


@dataclass
class Operation:
    operand_1: str = ""
    operator: str = ""
    operand_2: str = ""


@dataclass
class Monkey:
    number: int
    items: List[int] = field(default_factory=list)
    operation: Operation = Operation()
    div_by: int = 0
    if_true: int = 0
    if_false: int = 0
    inspect_cnt: int = 0


def parse_input(lines: List[str]) -> List[Monkey]:
    monkeys = []
    new_monkey = None
    for line in lines:
        if "Monkey" in line:
            new_monkey = Monkey(number=extract_all_ints(line).pop())
        elif "Starting items" in line:
            new_monkey.items = [x for x in extract_all_ints(line)]
        elif "Operation" in line:
            tokens = line.split('=')[1].split()
            new_monkey.operation = Operation(*tokens)
        elif "Test: divisible" in line:
            new_monkey.div_by = extract_all_ints(line).pop()
        elif "If true:" in line:
            new_monkey.if_true = extract_all_ints(line).pop()
        elif "If false:" in line:
            new_monkey.if_false = extract_all_ints(line).pop()
            monkeys.append(new_monkey)
    return monkeys


def solve(monkeys: List[Monkey], rounds: int = 10000, part2: bool = False) -> int:
    mod_op = reduce(lambda accu, m: accu * m.div_by, monkeys, 1) if part2 else None
    for _ in range(rounds):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                item = monkey.items.pop(0)
                op2 = item if monkey.operation.operand_2 == 'old' else int(monkey.operation.operand_2)
                if monkey.operation.operator == '+':
                    item = item + op2
                else:
                    item = item * op2
                item = item % mod_op if part2 else item // 3
                if (item % monkey.div_by) == 0:
                    monkeys[monkey.if_true].items.append(item)
                else:
                    monkeys[monkey.if_false].items.append(item)
                monkey.inspect_cnt += 1
    cnts = [-m.inspect_cnt for m in monkeys]
    heapq.heapify(cnts)
    return heapq.heappop(cnts) * heapq.heappop(cnts)


def part_1(monkeys: List[Monkey]) -> int:
    return solve(monkeys, 20, part2=False)


def part_2(monkeys: List[Monkey]) -> int:
    return solve(monkeys, 10000, part2=True)


def main():
    lines = get_lines("input_11.txt")
    monkeys = parse_input(lines)
    print("Part 1:", part_1(copy.deepcopy(monkeys)))  # 113232
    print("Part 2:", part_2(monkeys))  # 29703395016


if __name__ == '__main__':
    main()
    add(3, 1)
