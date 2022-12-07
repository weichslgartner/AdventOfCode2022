from dataclasses import dataclass

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
        tokenz = line.split(' ')
        if line.startswith('$'):
            cur_node = parse_command(cur_node, line, root, tokenz)
        else:
            parse_ls_output(cur_node, tokenz)
    return root


def parse_ls_output(cur_node, tokenz):
    size_or_dir, name = tokenz[0], tokenz[1]
    if size_or_dir == 'dir':
        if not cur_node.children:
            cur_node.children = {}
        if name not in cur_node.children.keys():
            child = Node(name, parent=cur_node)
            cur_node.children[name] = child
    else:
        if not cur_node.children:
            cur_node.children = {}
        if name not in cur_node.children.keys():
            child = Node(name, int(size_or_dir), is_file=True, parent=cur_node)
            cur_node.children[name] = child


def parse_command(cur_node, line, root, tokenz):
    if 'cd' in line:
        if tokenz[2] == '..':
            cur_node = cur_node.parent
        elif tokenz[2] == '/':
            cur_node = root
        else:
            if tokenz[2] not in cur_node.children.keys():
                child = Node(tokenz[2])
                cur_node.children[child.name] = child
            cur_node = cur_node.children[tokenz[2]]
    if 'ls' in line:
        pass
    return cur_node


def calc_sum(node, sizes):
    if node.is_file:
        return node.size
    sum_c = 0
    for child in node.children.values():
        sum_c += calc_sum(child, sizes)
    sizes.append(sum_c)
    return sum_c


def part_1(root):
    sizes = []
    _ = calc_sum(root, sizes)
    return sum(filter(lambda x: x < 100000, sizes))


def part_2(root):
    sizes = []
    cur_used = calc_sum(root, sizes)
    needed = SIZE_NEEDED - (TOTAL_SIZE - cur_used)
    return min(filter(lambda x: x > needed, sizes))


def main():
    lines = get_lines("input_07.txt")
    root = parse_input(lines)
    print("Part 1:", part_1(root)) # 1306611
    print("Part 2:", part_2(root)) # 13210366


if __name__ == '__main__':
    main()
