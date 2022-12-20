from copy import copy
from dataclasses import dataclass

from aoc import *
decryption_key = 811589153

class Node:
    def __init__(self,val,next,prev):
        self.val = val
        self.next = next
        self.prev = prev

    def insert_after(self,other):
        self.next, other.next, other.prev, self.next.prev = other, self.next, self, other
        other.prev = self
        print(other,self)

    def insert_before(self,other):
        self.prev, other.next, other.prev, self.prev.next = other, self, self.prev, other

        print(other,self)

    def remove(self):
        self.prev.next, self.next.prev  = self.next, self.prev
        print(self)

def parse_input(lines):
    head = None
    prev = None
    cur = None
    for n in list(map(int,lines)):
        cur = Node(val=n,prev=prev,next=None)
        if prev:
            prev.next = cur
        prev = cur
        if head is None:
            head = cur
    cur.next = head
    head.prev = cur

    return head, list(enumerate(map(int,lines)))


def solve(lines, rounds):
    length = len(lines)
    elements = lines.copy();
    for _ in range(rounds):
        for n in elements:
            old_index = lines.index(n)
            i = n[1]
            if i == 0:
                continue
            elif old_index + i < 0 or old_index + i >= length:
                new_index = (old_index + i) % (length - 1)
            else:
                new_index = (old_index + i)
            lines.insert(new_index if new_index else length - 1, lines.pop(old_index))
        idx = lines.index(list(filter(lambda x: x[1] == 0, lines)).pop())
    return sum(map(lambda x: x[1], (lines[(idx + grove) % length] for grove in [1000, 2000, 3000])))

def part_1(lines):
    return solve(lines,1)


def print_list(head):
    visited = set()
    cur = head
    while True:
        if cur in visited:
            break
        print(cur.val, end =",")
        visited.add(cur)
        cur = cur.next
    print()

def part_1_list(head, lines):
    length = len(lines)
    indices = {}
    cur = head
    for _ in range(length):
        indices[cur.val] = cur
        cur = cur.next
    print_list(head)
    for i in lines:
        el = indices[i]
        if i > 0:
            cur = el.next
            el.remove()
            for _ in range(i-1):
                cur = cur.next
            cur.insert_after(el)
        elif i < 0:
            cur = el.prev
            el.remove()
            for _ in range(abs(i) - 1):
                cur = cur.prev
            cur.insert_before(el)
        indices[i] = el
        print_list(el)
    return 0



def part_2(lines):
    lines = list(map(lambda x: (x[0],x[1]*decryption_key),lines))
    return solve(lines,10)


def main():
    lines = get_lines("input_20.txt") # too low 6711
    head, lines = parse_input(lines)
    #print("Part 1:", part_1(head, lines))
    print("Part 1:", part_1(lines.copy()))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
