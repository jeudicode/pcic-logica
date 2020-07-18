"""
BDD package
By Diego Isla-Lopez

PCIC - IIMAS @ UNAM
2020
"""


"""
TODO:
* set prefix notation
* terminals on input

"""




import sys
from node import Node
from graphviz import Digraph
from datetime import datetime
class BDD:

    def __init__(self, formula, order, root=None):
        self.formula = formula
        if order != None:
            self.order = [x for x in order]
        else:
            self.order = order

        self.node_count = 0
        if root == None:
            if len(self.formula) == 1:
                self.root = Node(label=self.order[0], id=2, index=1)
        else:
            self.root = root
        self.f_op = []
        self.f_vars = []

        if self.formula != None:
            if self.root.label not in self.order:
                print("foo")
                if self.root.label not in [0, 1]:
                    sys.exit("Not a terminal or variable in order")
            else:
                self.parse_formula()
                self.build_tree()

    def parse_formula(self):
        operators = ["+", "&", "-", "#"]
        for elem in self.formula:
            if elem in operators:
                self.f_op.append(elem)
            else:
                self.f_vars.append(elem)

    """
    Creates the initial tree
    """

    def build_tree(self, node=None, source=0, op=None):
        if node == None:
            node = self.root

        self.node_count += 1
        source_high = 1
        source_low = 0

        if len(self.f_op) == 0:
            if len(self.f_vars) == 0:
                pass
            else:
                fv = self.f_vars.pop(0)
                if node.label in ["0", "1"]:
                    pass
                else:
                    pass
        else:
            fop = self.f_op.pop(0)
            fv = self.f_vars.pop(0)

            if fop == "-":
                q_high = self.build_tree(Node(), 0, fop)
                q_low = self.build_tree(Node(), 1, fop)
            else:
                q_high = self.build_tree(Node(), 1, fop)
                q_low = self.build_tree(Node(), 0, fop)
        node.high = q_high
        node.low = q_low

        return node

    """
    Reduces current BDD
    """

    def _reduce(self, node=None):

        result = []
        nextid = 0

        levels = self.traverse()
        # print("levels: ", levels)
        # print("***************************")
        levels = levels[::-1]

        # print("levels reversed: ", levels)

        for level in levels:
            iso = {}  # for saving repeated subtrees

            for el in level:
                # print("el: " + str(el.label) + " " + str(el.value) + " " + str(el.index) +
                #       " " + str(el.low) + " " + str(el.high))
                if el.value != None:
                    key = str(el.value)
                elif el.low.id == el.high.id:
                    el.id = el.low.id
                    continue
                else:
                    key = str(el.low.id) + " " + str(el.high.id)

                if key in iso:
                    iso[key].append(el)
                else:
                    iso[key] = [el]

            for key, vertices in iso.items():
                for v in vertices:
                    v.id = nextid
                nextid += 1

                x = vertices[0]
                result.append(x)

                if x.index != None:
                    x.low = result[x.low.id]
                    x.high = result[x.high.id]

        self.node_count = len(result)
        if self.formula:
            self.create_graph(result, self.formula)
        else:
            self.create_graph(result, "result")

        # print("result: ", result)
        # print("root: ", result[-1].label)
        self.root = result[0]

    """
    Apply operator between current and a separate BDD
    """

    def apply(self, b1=None, b2=None, op=None, counter=0):
        if b1 == None:
            b1 = self.root

        if b1.label in [0, 1] and b2.label in [0, 1]:
            # both are terminals
            if op == "+":
                res = b1.label or b2.label
            elif op == "&":
                res = b1.label and b2.label
            elif op == "#":
                res = b1.label != b2.label

            if res == 1:
                # return self.ter_T
                return Node(label=1, id=1, value=1)
            else:
                # return self.ter_F
                return Node(label=0, id=0, value=0)
        else:  # labels are variables
            # subtrees have same root label
            if b1.label == b2.label:
                index = self.order.index(b1.label) + 1
                n = Node(label=b1.label, index=index, id=counter+2)
                counter += 1
                n.low = self.apply(b1.low, b2.low, op, counter)
                n.high = self.apply(b1.high, b2.high, op, counter)
            else:
                # not the same root
                if b1.label in self.order:
                    if b2.label in self.order:
                        # both non terminal
                        i1 = self.order.index(b1.label)
                        i2 = self.order.index(b2.label)

                        if i1 <= i2:
                            counter += 1
                            n = Node(label=b1.label,
                                     index=i1+1, id=counter+2)
                            n.low = self.apply(b1.low, b2, op, counter)
                            n.high = self.apply(b1.high, b2, op, counter)
                        elif i1 > i2:
                            n = Node(label=b2.label,
                                     index=i2+1, id=counter+2)
                            n.low = self.apply(b2.low, b1, op, counter)
                            n.high = self.apply(b2.high, b1, op, counter)
                    else:
                        # b2 is terminal
                        counter += 1
                        index = self.order.index(b1.label) + 1
                        n = Node(label=b1.label, index=index, id=counter+2)
                        if b1.low.label in [0, 1]:  # if no more subtrees
                            if op == "+":
                                res_low = b1.low.label or b2.label
                            elif op == "&":
                                res_low = b1.low.label and b2.label
                            elif op == "#":
                                res_low = b1.low.label != b2.label

                            if res_low == 1:
                                # n.low = self.ter_T
                                n.low = Node(label=1, id=1, value=1)
                            else:
                                # n.low = self.ter_F
                                n.low = Node(label=0, id=0, value=0)
                        else:
                            n.low = self.apply(b2, b1.low, op)

                        if b1.high.label in [0, 1]:  # if no more subtrees
                            if op == "+":
                                res_high = b1.high.label or b2.label
                            elif op == "&":
                                res_high = b1.high.label and b2.label
                            elif op == "#":
                                res_high = b1.high.label != b2.label

                            if res_high == 1:
                                #n.high = self.ter_T
                                n.high = Node(label=1, id=1, value=1)
                            else:
                                # n.high = self.ter_F
                                n.high = Node(label=0, id=0, value=0)
                        else:
                            n.high = self.apply(b2, b1.high, op)

                else:
                    # b1 is terminal
                    if b2.label in self.order:
                        # b2 is non terminal
                        counter += 1
                        index = self.order.index(b2.label) + 1
                        n = Node(label=b2.label, index=index, id=counter+2)
                        if b2.low.label in [0, 1]:  # if no more subtrees
                            if op == "+":
                                res_low = b2.low.label or b1.label
                            elif op == "&":
                                res_low = b2.low.label and b1.label
                            elif op == "#":
                                res_low = b2.low.label != b1.label

                            if res_low == 1:
                                # n.low = self.ter_T
                                n.low = Node(label=1, id=1, value=1)
                            else:
                                # n.low = self.ter_F
                                n.low = Node(label=0, id=0, value=0)
                        else:
                            n.low = self.apply(b1, b2.low, op, counter)

                        if b2.high.label in [0, 1]:  # if no more subtrees
                            if op == "+":
                                res_high = b2.high.label or b1.label
                            elif op == "&":
                                res_high = b2.high.label and b1.label
                            elif op == "#":
                                res_high = b2.high.label != b1.label

                            if res_high == 1:
                                # n.high = self.ter_T
                                n.high = Node(label=1, id=1, value=1)
                            else:
                                # n.high = self.ter_F
                                n.high = Node(label=0, id=0, value=0)
                        else:
                            n.high = self.apply(b1, b2.high, op, counter)

        return n

    """
    Return array of nodes by level
    """

    def traverse(self):
        def _traverse(v, levels):
            if v.index != None:
                levels[v.index-1].append(v)
                _traverse(v.low, levels)
                _traverse(v.high, levels)
            elif v.value != None:
                levels[len(levels)-1].append(v)

        levels = []
        for i in range(len(self.order)+1):
            levels.append([])
        _traverse(self.root, levels)
        return levels

    def _print(self, node=None):
        if node == None:
            node = self.root

        print(str(node.label))
        if node.low:
            print("low from " + node.label)
            self._print(node.low)

        if node.high:
            print("high from " + node.label)
            self._print(node.high)

        return node

    def create_graph(self, nodes, title):
        nodes.reverse()

        v = []
        e = []

        dot = Digraph(comment=title, format="png", name=title)

        for node in nodes:
            name = str(node.id)
            label = str(node.label)
            dot.node(name, label)

            if node.high != None and node.low != None:
                e1 = str(node.id) + str(node.high.id)
                e2 = str(node.id) + str(node.low.id)

                dot.edge(str(node.id), str(node.high.id))
                dot.edge(str(node.id), str(node.low.id), style="dashed")

        # print("Graph:")
        # print(dot.source)

        fname = "f" + title + "_" + str(datetime.now())
        dot.render(fname)
