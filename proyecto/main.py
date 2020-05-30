from bdd import BDD
import sys


if len(sys.argv) == 5:
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    op = sys.argv[3]
    order = sys.argv[4]

    b1 = BDD(f1, order)
    print("\nFormula for B1: ", b1.formula)
    print("\nOriginal B1:\n")
    b1._print()
    print("nodes in b1: ", b1.count_nodes())

    print("\nReducing B1:\n")
    b1._reduce()
    b1._print()
    print("nodes in b1: ", b1.node_count)

    b2 = BDD(f2, order)
    print("\nFormula for B2: ", b2.formula)
    print("\nOriginal B2:\n")
    b2._print()
    print("nodes in b2: ", b2.node_count)

    print("\nReducing B2:\n")
    b2._reduce()
    b2._print()
    print("nodes in b2: ", b2.node_count)

    print("\nApplying B1 " + op + " B2:\n")
    result = BDD(None, order, b1.apply(b1.root, b2.root, op))
    print("\nResult:\n")
    result._print()
    result._reduce()
    print("\nReduced result:\n")
    result._print()
    print("nodes in result: ", result.node_count)
else:
    sys.exit("Not enough arguments.")
