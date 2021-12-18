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
        
        node = successor_root
        while node.left is not None:
            node = node.left
        return node

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
        
        node = successor_root
        while node.right is not None:
            node = node.right
        return node

    def reduce(self) -> bool:
        if self.value is not None: # regular number
            if self.value >= 10:
                self.left = self.make_child(self.value // 2)
                self.right = self.make_child(math.ceil(self.value/2))
                self.value = None
                return True
            return False
        elif self.depth == 3:
            if self.left.value is None:
                self.right.value += self.left.right.value
                predecessor_leaf = self.predecessor_leaf_node()
                if predecessor_leaf is not None:
                    predecessor_leaf.value += self.left.left.value
                self.left = self.make_child(0)
                return True
            elif self.right.value is None:
                self.left.value += self.right.left.value
                successor_leaf = self.successor_leaf_node()
                if successor_leaf is not None:
                    successor_leaf.value += self.right.right.value
                self.right = self.make_child(0)
                return True
            else:
                return (self.left.reduce() or self.right.reduce())
        else:
            return (self.left.reduce() or self.right.reduce())

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        return f"[{self.left},{self.right}]"

def get_snails():
    text = Path("problem_18.txt").read_text().strip()
    return [Snail(literal_eval(line), depth=0) for line in text.split("\n")]

def part_a():
    snail = Snail([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]], 0, None)
    keep_reducing = True
    while keep_reducing:
        keep_reducing = snail.reduce()
        print(keep_reducing)
    print(snail)

print(part_a())