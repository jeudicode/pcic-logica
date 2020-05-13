"""
BDD package
By Diego Isla-Lopez

PCIC - IIMAS @ UNAM
2020
"""

import numpy as np
from node import Node


class BDD:

    def __init__(self, formula, order):
        self.formula = formula
        self.order = [x for x in order]
        self.terT = Node(1)
        self.terF = Node(0)
        self.root = Node(self.order[0])
        self.f_op = []

        self.parse_formula()
        self.build_tree()
        # self._reduce()

    """
    Creates the initial tree
    """

    def parse_formula(self):
        operators = ["+", "x", "!"]
        for elem in self.formula:
            if elem in operators:
                self.f_op.append(elem)

    def build_tree(self, node=None, counter=0, source=0, op=None):
        if node == None:
            node = self.root

        if counter == 0:  # dealing with root
            if self.f_op[counter] == "!":
                counter += 1
                op = self.f_op[counter - 1]
                q1 = self.build_tree(
                    Node(self.order[counter]), counter, 1, op)
                q2 = self.build_tree(
                    Node(self.order[counter]), counter, 0, op)
            else:
                counter += 1
                op = self.f_op[counter - 1]
                q1 = self.build_tree(Node(self.order[counter]), counter, 0, op)
                q2 = self.build_tree(Node(self.order[counter]), counter, 1, op)

        elif counter == len(self.order) - 1:  # dealing with last variable
            source_high = 1
            source_low = 0
            if counter == len(self.f_op):
                if op == "+":
                    source_high = source or source_high
                    source_low = source or source_low
                elif op == "x":
                    source_high = source and source_high
                    source_low = source and source_low

            else:
                if self.f_op[counter] == "!":
                    if op == "+":
                        source_high = source or not source_high
                        source_low = source or not source_low
                    elif op == "x":
                        source_high = source and not source_high
                        source_low = source and not source_low
                else:
                    if op == "+":
                        source_high = source or source_high
                        source_low = source or source_low
                    elif op == "x":
                        source_high = source and source_high
                        source_low = source and source_low

            if source_high == 1:
                q1 = self.terT
            else:
                q1 = self.terF

            if source_low == 1:
                q2 = self.terT
            else:
                q2 = self.terF

        else:  # dealing with intermediate variables
            if self.f_op[counter] == "!":
                source_high = 1
                source_low = 0
                if op == "+":
                    source_high = source or not source_high
                    source_low = source or not source_low
                elif op == "x":
                    source_high = source and not source_high
                    source_low = source and not source_low

                counter += 1
                op = self.f_op[counter - 1]
                q1 = self.build_tree(
                    Node(self.order[counter]), counter, source_high, op)
                q2 = self.build_tree(
                    Node(self.order[counter]), counter, source_low, op)
            else:
                source_high = 1
                source_low = 0
                if op == "+":
                    source_high = source or source_high
                    source_low = source or source_low
                elif op == "x":
                    source_high = source and source_high
                    source_low = source and source_low

                counter += 1
                op = self.f_op[counter - 1]
                q1 = self.build_tree(
                    Node(self.order[counter]), counter, source_high, op)
                q2 = self.build_tree(
                    Node(self.order[counter]), counter, source_low, op)

        node.high = q1
        node.low = q2

        return node

    def _reduce(self, node=None):
        if node == None:
            node = self.root

        if node.left.label not in [0, 1]:
            node.left = self._reduce(node.left)
        else:
            if node.left.label == node.right.label:
                return node.left

        if node.right.label not in [0, 1]:
            node.right = self._reduce(node.right)
        else:
            if node.left.label == node.right.label:
                return node.right

        return node

    def apply(self):
        pass
