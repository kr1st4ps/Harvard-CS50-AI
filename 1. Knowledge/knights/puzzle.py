from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    #   A is either but not both
    And(Or(AKnave, AKnight), Not(And(AKnight, AKnave))),

    #   A is a knight if and only if his statement is true
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #   A and B are either but not both
    And(Or(AKnave, AKnight), Not(And(AKnight, AKnave))),
    And(Or(BKnave, BKnight), Not(And(BKnight, BKnave))),

    #   A is a knight if and only if his statement is true
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #   A and B are either but not both
    And(Or(AKnave, AKnight), Not(And(AKnight, AKnave))),
    And(Or(BKnave, BKnight), Not(And(BKnight, BKnave))),

    #   A is a knight if and only if his statement is true
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    #   B is a knight if and only if his statement is true
    Biconditional(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave)))
    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    #   A, B and C are either but not both
    And(Or(AKnave, AKnight), Not(And(AKnight, AKnave))),
    And(Or(BKnave, BKnight), Not(And(BKnight, BKnave))),
    And(Or(CKnave, CKnight), Not(And(CKnight, CKnave))),

    #   If B is a knight, then A says "I am a knave.". Therefore A is a knight if and only if his statement is true
    Implication(BKnight, Biconditional(AKnight, AKnave)),

    #   If B is a knave, then A says "I am a knight.". Therefore A is a knight if and only if his statement is true
    Implication(BKnave, Biconditional(AKnight, AKnight)),

    #   B is a knight if and only if his statement that C is a knave is true
    Biconditional(BKnight, CKnave),

    #   C is a knight if and only if his statement that A is a knight is true
    Biconditional(CKnight, AKnight)
)



def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
