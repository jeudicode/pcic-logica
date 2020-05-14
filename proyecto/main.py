from bdd import BDD
import sys


if len(sys.argv) == 5:
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    op = sys.argv[3]
    order = sys.argv[4]

    # if f1[0] not in operators:
    #     sys.exit("Invalid formula")
    # else:
    #     for (i, sym) in enumerate(f1):
    #         print(sym)

    b1 = BDD(f1, order)
    print("Formula for B1: ", b1.formula)
    print("\nOriginal B1:\n")
    b1._print()
    # print(b1.a)
    b2 = BDD(f2, order)
    print("Formula for B2: ", b2.formula)
    print("\nOriginal B2:\n")
    b2._print()
    b1._reduce()
    print("\nReducing B1:\n")
    b1._print()
    print("\nReducing B2:\n")
    b2._reduce()
    b2._print()
    # print(b2.a)
    print("\nApplying B1 " + op + " B2:\n")
    result = BDD(None, None, b1.apply(b1.root, b2.root, op))
    result._reduce()
    result._print()
else:
    sys.exit("Not enough arguments.")

# +(p,+(qr))
