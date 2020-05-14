"""
BDD package
By Diego Isla-Lopez

PCIC - IIMAS @ UNAM
2020
"""

import numpy as np
from node import Node


class BDD:

    def __init__(self, formula, order, root=None):
        self.formula = formula
        if order != None:
            self.order = [x for x in order]
        else:
            self.order = order
        self.ter_T = Node(1)
        self.ter_F = Node(0)
        if root == None:
            self.root = Node(self.order[0])
        else:
            self.root = root
        self.f_op = []

        if self.formula != None:
            self.parse_formula()
            self.build_tree()
        # self._reduce()

    """
    Creates the initial tree
    """

    def parse_formula(self):
        operators = ["+", "x", "-", "#"]
        for elem in self.formula:
            if elem in operators:
                self.f_op.append(elem)

    def build_tree(self, node=None, counter=0, source=0, op=None):
        if node == None:
            node = self.root

        source_high = 1
        source_low = 0

        if counter == 0:  # dealing with root
            if self.f_op[counter] == "-":
                counter += 1
                op = self.f_op[counter]
                q_high = self.build_tree(
                    Node(self.order[counter]), counter, 0, op)
                q_low = self.build_tree(
                    Node(self.order[counter]), counter, 1, op)
            else:
                counter += 1
                op = self.f_op[counter - 1]
                q_high = self.build_tree(
                    Node(self.order[counter]), counter, 1, op)
                q_low = self.build_tree(
                    Node(self.order[counter]), counter, 0, op)

        elif counter == len(self.order) - 1:  # dealing with last variable
            if counter == len(self.f_op):
                if op == "+":
                    source_high = source or source_high
                    source_low = source or source_low
                elif op == "x":
                    source_high = source and source_high
                    source_low = source and source_low
                elif op == "#":
                    source_high = source != source_high
                    source_low = source != source_low

            else:
                if self.f_op[counter] == "-":
                    if op == "+":
                        source_high = source or not source_high
                        source_low = source or not source_low
                    elif op == "x":
                        source_high = source and not source_high
                        source_low = source and not source_low
                    elif op == "#":
                        source_high = source != (not source_high)
                        source_low = source != (not source_low)
                else:
                    if op == "+":
                        source_high = source or source_high
                        source_low = source or source_low
                    elif op == "x":
                        source_high = source and source_high
                        source_low = source and source_low
                    elif op == "#":
                        source_high = source != source_high
                        source_low = source != source_low

            if source_high == 1:
                q_high = self.ter_T
            else:
                q_high = self.ter_F

            if source_low == 1:
                q_low = self.ter_T
            else:
                q_low = self.ter_F

        else:  # dealing with intermediate variables
            if self.f_op[counter] == "-":
                if op == "+":
                    source_high = source or not source_high
                    source_low = source or not source_low
                elif op == "x":
                    source_high = source and not source_high
                    source_low = source and not source_low
                elif op == "#":
                    source_high = source != (not source_high)
                    source_low = source != (not source_low)

                counter += 1
                op = self.f_op[counter]
                q_high = self.build_tree(
                    Node(self.order[counter]), counter, source_high, op)
                q_low = self.build_tree(
                    Node(self.order[counter]), counter, source_low, op)
            else:
                if op == "+":
                    source_high = source or source_high
                    source_low = source or source_low
                elif op == "x":
                    source_high = source and source_high
                    source_low = source and source_low
                elif op == "#":
                    source_high = source != source_high
                    source_low = source != source_low

                counter += 1
                op = self.f_op[counter - 1]
                q_high = self.build_tree(
                    Node(self.order[counter]), counter, source_high, op)
                q_low = self.build_tree(
                    Node(self.order[counter]), counter, source_low, op)

        node.high = q_high
        node.low = q_low

        return node

    def _reduce(self, node=None):
        if node == None:
            node = self.root

        if node.low != None:
            if node.low.label not in [0, 1]:
                node.low = self._reduce(node.low)
            else:
                if node.low.label == node.high.label:
                    return node.low

        if node.high != None:
            if node.high.label not in [0, 1]:
                node.high = self._reduce(node.high)
            else:
                if node.low.label == node.high.label:
                    return node.high

        if node.low.label == node.high.label:
            return node.high

        return node

    def apply(self, b1=None, b2=None, op=None):
        if b1 == None:
            b1 = self.root

        if b1.label in [0, 1] and b2.label in [0, 1]:
            # both are terminals
            if op == "+":
                res = b1.label or b2.label
            elif op == "x":
                res = b1.label and b2.label
            elif op == "#":
                res = b1.label != b2.label

            if res == 1:
                return self.ter_T
            else:
                return self.ter_F
        else:  # labels are variables
            # subtrees have same root label
            if b1.label == b2.label:
                n = Node(b1.label)
                n.low = self.apply(b1.low, b2.low, op)
                n.high = self.apply(b1.high, b2.high, op)
            else:
                # not the same root
                if b1.label in self.order:
                    if b2.label in self.order:
                        # both non terminal
                        i1 = self.order.index(b1.label)
                        i2 = self.order.index(b2.label)

                        if i1 < i2:
                            n = Node(b1.label)
                            n.low = self.apply(b1.low, b2, op)
                            n.high = self.apply(b1.high, b2, op)
                        elif i1 > i2:
                            n = Node(b2.label)
                            n.low = self.apply(b2.low, b1, op)
                            n.high = self.apply(b2.high, b1, op)
                    else:
                        # b2 is terminal
                        n = Node(b1.label)
                        if b1.low.label in [0, 1]:  # if no more subtrees
                            if op == "+":
                                res_low = b1.low.label or b2.label
                                #res_high = b1.high.label or b2.label
                            elif op == "x":
                                res_low = b1.low.label and b2.label
                                #res_high = b1.high.label and b2.label

                            if res_low == 1:
                                n.low = self.ter_T
                            else:
                                n.low = self.ter_F
                        else:
                            n.low = self.apply(b2, b1.low, op)

                        if b1.high.label in [0, 1]:  # if no more subtrees
                            if op == "+":
                                res_high = b1.high.label or b2.label
                                #res_high = b1.high.label or b2.label
                            elif op == "x":
                                res_high = b1.high.label and b2.label
                                #res_high = b1.high.label and b2.label

                            if res_high == 1:
                                n.high = self.ter_T
                            else:
                                n.high = self.ter_F
                        else:
                            n.high = self.apply(b2, b1.high, op)

                else:
                    # b1 is terminal
                    if b2.label in self.order:
                        # b2 is non terminal
                        n = Node(b2.label)
                        if b2.low.label in [0, 1]:  # if no more subtrees
                            if op == "+":
                                res_low = b2.low.label or b1.label
                                #res_high = b1.high.label or b2.label
                            elif op == "x":
                                res_low = b2.low.label and b1.label
                                #res_high = b1.high.label and b2.label

                            if res_low == 1:
                                n.low = self.ter_T
                            else:
                                n.low = self.ter_F
                        else:
                            n.low = self.apply(b1, b2.low, op)

                        if b2.high.label in [0, 1]:  # if no more subtrees
                            if op == "+":
                                res_high = b2.high.label or b1.label
                                #res_high = b1.high.label or b2.label
                            elif op == "x":
                                res_high = b2.high.label and b1.label
                                #res_high = b1.high.label and b2.label

                            if res_high == 1:
                                n.high = self.ter_T
                            else:
                                n.high = self.ter_F
                        else:
                            n.high = self.apply(b1, b2.high, op)

        return n

    def _print(self, node=None):
        if node == None:
            node = self.root

        print(node.label)
        if node.low:
            print("low from " + node.label)
            self._print(node.low)

        if node.high:
            print("high from " + node.label)
            self._print(node.high)

        return node
