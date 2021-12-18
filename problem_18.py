import math
from ast import literal_eval
from pathlib import Path
from typing import List, Optional, Union

RawSnail = Union[int, List["RawSnail"]]

class Snail:
    def __init__(self, raw_snail: RawSnail, depth: int, parent: Optional[RawSnail]):
        self.depth = depth
        self.parent = parent
        if isinstance(raw_snail, list):
            assert len(raw_snail) == 2
            self.value = None
            self.left = self.make_child(raw_snail[0])
            self.right = self.make_child(raw_snail[1])
        else:
            self.value = raw_snail
            self.left = self.right = None

    def increment_depth(self):
        self.depth += 1
        if self.left:
            self.left.increment_depth()
        if self.right:
            self.right.increment_depth()

    def magnitude(self):
        if self.value is not None:
            return self.value
        return (3 * self.left.magnitude()) + (2 * self.right.magnitude())

    def make_child(self, new_snail: RawSnail):
        return Snail(new_snail, self.depth + 1, self)

    def successor_leaf_node(self):
        node = self
        while True:
            if node.parent is None:
                return None
            if node is node.parent.right:
                node = node.parent
                continue
            successor_root = node.parent.right
            break
        
        return successor_root.leftmost()

    def predecessor_leaf_node(self):
        node = self
        while True:
            if node.parent is None:
                return None
            if node is node.parent.left:
                node = node.parent
                continue
            successor_root = node.parent.left
            break
        
        return successor_root.rightmost()

    def leftmost(self):
        if self.is_leaf:
            return self
        return self.left.leftmost()

    def rightmost(self):
        if self.is_leaf:
            return self
        return self.right.rightmost()

    @property
    def is_leaf(self):
        return self.value is not None

    def split(self):
        if self.is_leaf:
            if self.value >= 10:
                self.left = self.make_child(self.value // 2)
                self.right = self.make_child(math.ceil(self.value/2))
                self.value = None
                return True
            return False
        else:
            return (self.left.split() or self.right.split())

    def can_explode(self):
        if self.is_leaf:
            return False
        if self.depth >= 3 and not (self.left.is_leaf and self.right.is_leaf):
            return True
        return self.left.can_explode() or self.right.can_explode()

    def can_split(self):
        if self.is_leaf:
            return self.value >= 10
        return self.left.can_split() or self.right.can_split()

    def explode(self) -> bool:  # returns whether a change took place.
        if self.is_leaf:
            return False
        if self.left.explode():
            return True
        if self.depth >= 3:
            if not self.left.is_leaf:  # try exploding this first
                next_node_right = self.right.leftmost()
                next_node_right.value += self.left.right.value
                predecessor_leaf = self.predecessor_leaf_node()
                if predecessor_leaf is not None:
                    predecessor_leaf.value += self.left.left.value
                self.left = self.make_child(0)
                return True
            elif not self.right.is_leaf:
                next_node_left = self.left.rightmost()
                next_node_left.value += self.right.left.value
                successor_leaf = self.successor_leaf_node()
                if successor_leaf is not None:
                    successor_leaf.value += self.right.right.value
                self.right = self.make_child(0)
                return True
        return self.right.explode()

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        return f"[{self.left},{self.right}]"

def get_snails():
    text = Path("problem_18.txt").read_text().strip()
    return [Snail(literal_eval(line), depth=0, parent=None) for line in text.split("\n")]

def add_snails(first: Snail, second: Snail):
    first.increment_depth()
    second.increment_depth()
    base_snail = Snail(0, 0, None)
    first.parent = second.parent = base_snail
    base_snail.left = first
    base_snail.right = second
    base_snail.value = None
    return base_snail


def reduce_snail(snail: Snail):
    while True:
        if snail.can_explode():
            snail.explode()
        elif snail.can_split():
            snail.split()
        else:
            break


def part_a():
    snails = get_snails()
    snail_so_far = snails.pop(0)
    for new_snail in snails:
        snail_so_far = add_snails(snail_so_far, new_snail)
        reduce_snail(snail_so_far)
    return snail_so_far.magnitude()

print(part_a())
