# - LEVENSHTEIN.PY -----------------------------------------------------#
#    Routines to calculate Levenshtein distance, report optimal ops to  #
#    convert between strings, and to use BK-trees to find words from a  #
#    set of words that are within a threshold Levenstein distance to a  #
#    target word                                                        #
#                                                                       #
# - When: ------ Who: ------------------ Comments: ---------------------#
#                                                                       #
#  27-Aug-23    Christopher G. Healey   Initial implementation          #
# ----------------------------------------------------------------------#

#  Python libraries

import json


def describe(a, b, op):
    """Describe a->b character op by character op

    Args:
        a (string): Source word
        b (string): Target word
        op (dictionary): Operations to convert source to target
    """

    i = len(a)
    j = len(b)
    cur_word = a

    print(f"Levenshtein distance: {D[i][j]}\n")

    while i != 0 or j != 0:  # While not at front of both words
        if op[i][j]["op"] == "I":  # Insert
            i, j = op[i][j]["pos"]  # Position insert occurred
            print(f"{cur_word} -> ", end="")
            cur_word = cur_word[:i] + b[j] + cur_word[i:]
            print(f"{cur_word} (I)")

        elif op[i][j]["op"] == "D":  # Delete
            i, j = op[i][j]["pos"]  # Position deletion occurred
            print(f"{cur_word} -> ", end="")
            cur_word = cur_word[:i] + cur_word[i + 1 :]
            print(f"{cur_word} (D)")

        elif op[i][j]["op"] == "R":  # Replacement
            i, j = op[i][j]["pos"]  # Position replacement occurred
            print(f"{cur_word} -> ", end="")
            cur_word = cur_word[:i] + b[j] + cur_word[i + 1 :]
            print(f"{cur_word} (R)")

        else:  # Equivalence, back up to where equivalence occurred
            i, j = op[i][j]["pos"]

    print()


# End function describe


def find(root, tol, w, match):
    """Find all entries in a BK tree that are within a Levenshtein tolerance

    Args:
        root (dict): Root of BK tree
        tol (int): Allowed Levenshtein tolerance
        w (string): Word to compare tree entries against
        match (list of string): Tree entries within tolerance of target word

    Returns:
        list of string: Tree entries within tolerance of target word
    """

    dist = levenshtein(root["val"], w)  # Check if root of BK tree is a match
    if dist <= tol:
        match += [(dist, root["val"])]

    lo = dist - tol  # Calculate child range of Levenshtein values to check
    hi = dist + tol

    for k, v in root["child"].items():  # For all child nodes in tree
        # If child Levenshtein value in range, check subtree rooted at child

        if k >= lo and k <= hi:
            match = find(root["child"][k], tol, w, match)

    return match  # Return words within given tolerance


# End function find


def insert(root, w, desc=False):
    """Insert a new word into a BK tree

    Args:
        root (dict): Root of BK tree
        w (string): Word to insert
        desc (bool, option):  Describe a -> b character op by op.
                              Defaults to False.

    Returns:
        dict: Possibly new root of BK tree
    """

    if root == {}:  # (Sub)tree is empty?
        root["val"] = w  # Build root node for BK tree
        root["dist"] = 0
        root["child"] = {}
        return root

    d = levenshtein(root["val"], w, desc)  # Levenshtein distance to root's word
    if d == 0:  # Same word as at root?
        return root

    cur_root = root
    while cur_root != {}:  # Traverse child nodes in tree
        cur_d = levenshtein(cur_root["val"], w, desc)
        if cur_d == 0:  # Word already in tree?
            return root  # If so, return tree unaltered

        # If the given Levenshtein distance has not been added to a child
        # of the root, add it as a new child and return the altered tree

        if cur_d not in cur_root["child"]:  # No child w/Levenshtein distance?
            cur_root["child"][cur_d] = {  # Create child
                "val": w,
                "dist": cur_d,
                "child": {},
            }
            return root

        # Otherwise child w/Levenshtein distance already in tree, so
        # must insert beneath child

        cur_root = cur_root["child"][cur_d]

    print("insert(), unexpected exit from insertion loop")
    return root


# End function insert


def levenshtein(a, b, desc=False):
    """Calculate levenshtein distance between two words

    Args:
        a (string): First word
        b (string): Second word
        desc (bool, option):  Describe a -> b character op by op.
                              Defaults to False.

    Returns:
        int: Levenshtein(a,b)
    """

    if desc:
        print(f"{a} -> {b}:")

    # Initialiize distance matrix to all 0s, a's chars on rows, b's chars
    # on columns

    D = [[0 for i in range(0, len(b) + 1)] for j in range(0, len(a) + 1)]

    # Initialize operation used to calculate a given value in distance matrix
    # "op": operation applied (None,I=insert,D=delete,R=replace,E=equivalent)

    op = [
        [{"op": None, "pos": (0, 0)} for i in range(0, len(b) + 1)]
        for j in range(0, len(a) + 1)
    ]

    # Initialize first row and column to 1..m, 1..n

    for i in range(0, len(a) + 1):
        D[i][0] = i
        # op[i][0]["pos"] = (i, 0)
    for j in range(0, len(b) + 1):
        D[0][j] = j
        # op[0][j]["pos"] = (0, j)

    for i in range(1, len(a) + 1):  # For all rows
        for j in range(1, len(b) + 1):  # For allcolumns
            if a[i - 1] == b[j - 1]:  # If first char matches, substitution..
                sub = 0  # ..cost is 0
            else:
                sub = 1  # ..otherwise cost is 1 (swap)

            insert = 1 + D[i][j - 1]  # Cost of insert, delete, replace
            delete = 1 + D[i - 1][j]
            replace = D[i - 1][j - 1] + sub

            # Find operation with minimum cost

            D[i][j] = min(insert, delete, replace)

            if D[i][j] == insert:  # Record operation with minimum cost
                op[i][j]["op"] = "I"
                op[i][j]["pos"] = (i, j - 1)
            elif D[i][j] == delete:
                op[i][j]["op"] = "D"
                op[i][j]["pos"] = (i - 1, j)
            else:
                if sub == 0:
                    op[i][j]["op"] = "E"
                else:
                    op[i][j]["op"] = "R"
                op[i][j]["pos"] = (i - 1, j - 1)

    # If requested, print operations and how it modifies source s character
    # by character into target b

    if desc:
        describe(a, b, op)

    return D[len(a)][len(b)]


# End function levenshtein


# Mainline

with open("dictionary.json") as inp:  # Read JSON word file
    data = json.load(inp)
word = list(data.keys())
# with open("words.json") as inp:  # Read JSON word file
#    data = json.load(inp)
# word = data["data"]

n = len(word)  # Size of dictionary
step = n / 10  # Step size for reporting progress of insert
root = {}  # Construct BK-tree from list of words in JSON file

report = step
for i, w in enumerate(word):
    root = insert(root, w)
    if i > report:
        print(f"{i} of {n} words inserted...")
        report += step
print(f"{n} of {n} words inserted...")

done = False
while not done:  # Continue searching for words until user quits
    tg = input("Enter a target word: ")
    epsilon = input("Enter a positive threshold > 0: ")
    while not epsilon.isdigit():
        print("Threshold must be an integer > 0")
        epsilon = input("Enter a positive threshold > 0: ")
    epsilon = int(epsilon)

    candidate = find(root, epsilon, tg, [])  # Search for candidate words

    candidate = sorted(candidate)  # Sort by first entry of tuple, Levenshtein distance
    print("Candidates: ")
    print(candidate)

    cont = ""
    while cont != "Y" and cont != "N":
        cont = input("Would you like to enter another word (Y/N): ")
        cont = cont.upper()
    done = cont == "N"

print("Done")
