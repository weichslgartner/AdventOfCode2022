from dataclasses import dataclass, field
from operator import add
from typing import List

from aoc import get_lines, extract_all_ints
from pathlib import Path


@dataclass
class Operation:
    operand_1: str = ""
    operator: str = ""
    operand_2: str = ""


@dataclass
class Monkey:
    number: int
    items: List[int] =  field(default_factory=list)
    operation: Operation = Operation()
    div_by: int = 0
    if_true: int = 0
    if_false: int = 0
    inspect_cnt : int = 0


def parse_input(lines):
    # Monkey 1:
    #   Starting items: 54, 65, 75, 74
    #   Operation: new = old + 6
    #   Test: divisible by 19
    #     If true: throw to monkey 2
    #     If false: throw to monkey 0
    monkeys = {}
    for line in lines:
        #new_monkey : Monkey = None
        if "Monkey" in line:
            new_monkey = Monkey(number=extract_all_ints(line).pop())
        elif "Starting items" in line:
            new_monkey.items = extract_all_ints(line)
        elif "Operation" in line:
            tokens = line.split('=')[1].split()
            new_monkey.operation = Operation(*tokens)
        elif "Test: divisible" in line:
            new_monkey.div_by = extract_all_ints(line).pop()
        elif "If true:" in line:
            new_monkey.if_true = extract_all_ints(line).pop()
        elif "If false:" in line:
            new_monkey.if_false = extract_all_ints(line).pop()
            monkeys[new_monkey.number] = new_monkey
    print(monkeys)
    return monkeys


def part_1(monkeys, rounds = 20):
    for _ in range(rounds):
        for key, monkey in monkeys.items():
            while len(monkey.items) > 0:
                item = monkey.items.pop(0)
                op2 = item  if monkey.operation.operand_2 == 'old' else int(monkey.operation.operand_2)
                if monkey.operation.operator == '+':
                    item = item + op2
                else:
                    item = item * op2
                item //= 3
                if (item % monkey.div_by) == 0:
                    monkeys[monkey.if_true].items.append(item)
                else:
                    monkeys[monkey.if_false].items.append(item)
                monkey.inspect_cnt +=1

    print(monkeys)
    counts =  sorted([m.inspect_cnt for m in monkeys.values()],reverse=True)
    return counts[0]*counts[1]


def part_2(lines):
    pass


def main():
    lines = get_lines("input_11.txt")
    monkeys = parse_input(lines)
    print("Part 1:", part_1(monkeys))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
    add(3,1)
