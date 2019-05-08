# coding=utf-8
from Node import Node, LeafNode, Pair
from B_tree import B_tree, MAX_INT
from random import randint
from time import time

B_size = 3
b = B_tree(B_size)
b.insert(2, 78)
b.insert(3, 143)
b.insert(1, 123213)

print(b.get(1))
print(b.get(2))
print(b.get(3))
