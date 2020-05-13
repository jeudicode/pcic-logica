from bdd import BDD
import sys

operators = ["+", "&", "!"]

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
    print(b1.formula)
    # print(b1.a)
    b2 = BDD(f2, order)
    print(b2.formula)
    # print(b2.a)
    # b2 = BDD(f2)
    # res = b1.apply(op, b2)
    # print(res)
else:
    sys.exit("Not enough arguments.")

# +(p,+(qr))
