from dataclasses import dataclass
from typing import List

from aoc import get_lines

TOTAL_SIZE = 70000000

SIZE_NEEDED = 30000000


@dataclass
class Node:
    name: str
    size: int = 0
    is_file: bool = False
    parent: 'Node' = None
    children: dict[str, 'Node'] = None


def parse_input(lines):
    root = Node('/')
    cur_node = root
    for line in lines:
        tokenz = line.split()
        if line.startswith('$'):
            cur_node = parse_command(cur_node=cur_node, root=root, line=line, tokenz=tokenz)
        else:
            parse_ls_output(cur_node=cur_node, tokenz=tokenz)
    return root


def parse_ls_output(cur_node, tokenz):
    size_or_dir, name = tokenz[0], tokenz[1]
    if size_or_dir == 'dir':
        if not cur_node.children:
            cur_node.children = {}
        if name not in cur_node.children.keys():
            child = Node(name=name, parent=cur_node)
            cur_node.children[name] = child
    else:
        if not cur_node.children:
            cur_node.children = {}
        if name not in cur_node.children.keys():
            child = Node(name=name, size=int(size_or_dir), is_file=True, parent=cur_node)
            cur_node.children[name] = child


def parse_command(cur_node: Node, root: Node, line: str, tokenz: List[str]) -> Node:
    if 'cd' in line:
        folder = tokenz[2]
        if folder == '..':
            return cur_node.parent
        if folder == '/':
            return root
        if folder not in cur_node.children.keys():
            child = Node(folder)
            cur_node.children[child.name] = child
        return cur_node.children[folder]
    if 'ls' in line:
        pass
    return cur_node


def calc_sum(node: Node, sizes: List[int]) -> int:
    if node.is_file:
        return node.size
    sum_c = 0
    for child in node.children.values():
        sum_c += calc_sum(child, sizes)
    sizes.append(sum_c)
    return sum_c


def part_1(root: Node) -> int:
    sizes = []
    _ = calc_sum(root, sizes)
    return sum(filter(lambda x: x < 100000, sizes))


def part_2(root: Node) -> int:
    sizes = []
    cur_used = calc_sum(root, sizes)
    needed = SIZE_NEEDED - (TOTAL_SIZE - cur_used)
    return min(filter(lambda x: x > needed, sizes))


def main():
    lines = get_lines("input_07.txt")
    root = parse_input(lines)
    print("Part 1:", part_1(root))  # 1306611
    print("Part 2:", part_2(root))  # 13210366


if __name__ == '__main__':
    main()
