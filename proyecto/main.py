from bdd import BDD
import sys

if len(sys.argv) == 6:
    f1 = sys.argv[1]
    o1 = sys.argv[2]
    f2 = sys.argv[3]
    o2 = sys.argv[4]
    op = sys.argv[5]

    if op not in [',','$','x','-','/']:
        sys.exit("Invalid operator.")
    else:
        b1 = BDD(f1, o1)
        b2 = BDD(f2, o2)
        b1.apply(b2, op)
else:
    sys.exit("Not enough arguments.")    

