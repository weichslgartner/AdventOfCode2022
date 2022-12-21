from dataclasses import dataclass
from operator import add, mul, truediv, sub, floordiv

from aoc import get_lines

HUMN = 'humn'


@dataclass
class Node:
    name: str
    value: int = None
    operator: str = None
    left: 'Node' = None
    right: 'Node' = None


op_fun = {'+': add, '/': floordiv, '-': sub, '*': mul, }
op_fun_inv_left = {'+': sub, '/': mul, '-': add, '*': floordiv, '=': add}


def inv_right(op, target, left):
    if op == '+':
        return target - left
    if op == '-':
        return left - target
    if op == '*':
        return target // left
    if op == '/':
        return left // target


def parse_input(lines):
    node_dict = {}
    for line in lines:
        tokens = line.split(":")
        node = Node(name=tokens[0])
        rhs = tokens[1].split()
        if len(rhs) == 1:
            node.value = int(rhs[0].strip())
        else:
            node.left = rhs[0]
            node.operator = rhs[1]
            node.right = rhs[2]
        node_dict[node.name] = node
    for node in node_dict.values():
        if node.right:
            node.right = node_dict[node.right]
            node.left = node_dict[node.left]
    return node_dict["root"]


def calc(node: Node) -> int:
    if node.value:
        return node.value
    return op_fun[node.operator](calc(node.left), calc(node.right))


def tree_contains(node: Node, name):
    if node is None:
        return False
    if node.value:
        return node.name == name
    return tree_contains(node.left, name) or tree_contains(node.right, name)


def solve(node, target=0):
    if node.left.name == HUMN:
        return op_fun_inv_left[node.operator](target, calc(node.right))
    if node.right.name == HUMN:
        return inv_right(node.operator, target, left=calc(node.left))
    if not node.value:
        if tree_contains(node.left, HUMN):
            res = calc(node.right)
            target = op_fun_inv_left[node.operator](target, res)
            return solve(node.left, target)
        else:
            res = calc(node.left)
            target = inv_right(node.operator, target, left=res)
            return solve(node.right, target)


def part_1(root):
    return int(calc(root))


def part_2(root):
    return solve(root)


def main():
    lines = get_lines("input_21.txt")
    root = parse_input(lines)
    print("Part 1:", part_1(root))  # 63119856257960
    root.operator = '='
    print("Part 2:", part_2(root))  # 3006709232464


if __name__ == '__main__':
    main()
