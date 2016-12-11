# Overview

Generate random integers and compute odds using dice notation.

# How to Run

    $ pip install virtualenv

    $ make ve

    $ ./bin/roll.sh 3d6
    12

    $ ./bin/odds.sh 3d6
    3: (0.463%)
    4: (1.389%)
    5: (2.778%)
    6: (4.630%)
    7: (6.944%)
    8: (9.722%)
    9: (11.574%)
    10: (12.500%)
    11: (12.500%)
    12: (11.574%)
    13: (9.722%)
    14: (6.944%)
    15: (4.630%)
    16: (2.778%)
    17: (1.389%)
    18: (0.463%)

# Dice Notation

Generate random integers in the range 1–4, 1–6, 1–8, 1–12, and 1–20:

    d4 d6 d8 d12 d20

Generate a random integer in the range 2–7:

    d6+1

Generate a random integer in the range 1–100:

    d100

Generate a random integer in the range 0–99:

    d100-1

Generate three random integers in the range 1–6 and add them:

    3d6

Roll 4 sixers and keep the highest 3:

    4d6k3

Equivalently, roll 4 sixers and drop the lowest:

    4d6d1

It is possible to be explicit about whether high or low dice are kept or dropped:

    4d6kh3
    4d6kl3
    4d6dl1
    436dh1

# Odds

The code for computing odds is in `dice/odds.py`.

Probabilities can be exact using the `fractions.Fraction` type from
the Python standard library or approximate using the `float` type.
This is controlled by setting the `Probability` type and the
`probability` constructor in `dice/odds.py`.

An integer-valued random variable type is needed for storing dice
notation odds. The following typedefs are used:

    RV:      List[Tuple[int, Probability]]
    IterRV:  Iterable[Tuple[int, Probability]]

These functions return `RV` values:

    dice_notation_rv():     returns RV for dice notation.

    dedupe_rv():            makes sure each integer appears at most once in the list.
                            If an integer appears multiple times, the probabilities are
                            summed in the return value.

    sum_rv():               returns RV obtained by summing two RVs.

    multiply_scalar_rv():   returns RV obtained by applying scalar multiplication to RV.

    die_rv():               returns RV for rolling N dice with M faces.

    keep_high_rv():         returns RV for rolling N dice with M faces, keeping highest K.

    sum_mrv_rv():           returns RV obtained by summming RVs in a MRV.

A multivariate random variable type is needed for storing multiple
dice rolls, such as are used to generate attributes. The following
typedefs are used:

    MRV:      List[Tuple[List[int], Probability]]
    IterMRV:  Iterable[Tuple[List[int], Probability]]

These functions return `MRV` values:

    dedupe_mrv():             removes duplicates in an MRV by summing probabilities.

    tail_mrv():               takes the last N values of each List[int] in an MRV.
                              This may introduce duplicates.

    sorted_mrv():             sorts each List[int] in an MRV. This may introduce
                              duplicates.

    cartesian_product_mrv():  returns Cartesian product of an MRV and an RV.
