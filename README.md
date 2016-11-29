# Overview

Generate random numbers using dice notation.

# How to Run

    $ pip install virtualenv

    $ make ve

    $ ./bin/roll.sh 3d6
    12

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

Compute the odds for dice notation:

    $ ./bin/odds.sh 4d6kh3
    3: (0.077%)
    4: (0.309%)
    5: (0.772%)
    6: (1.620%)
    7: (2.932%)
    8: (4.784%)
    9: (7.022%)
    10: (9.414%)
    11: (11.420%)
    12: (12.886%)
    13: (13.272%)
    14: (12.346%)
    15: (10.108%)
    16: (7.253%)
    17: (4.167%)
    18: (1.620%)

The code is in `dice/odds.py`. Probabilities can be exact using the
`fractions.Fraction` from the Python standard library or approximate
using the `float` type.  This is controlled by setting the
`Probability` type and the `probability` constructor in
`dice/odds.py`.

An integer-valued random variable type is needed for storing dice
notation odds. The following typedefs are used:

    RV:      List[Tuple[int, Probability]]
    IterRV:  Iterable[Tuple[int, Probability]]

These functions return `RV` values:

    dice_notation_rv(): returns RV for dice notation.

    dedupe_rv():        makes sure each integer appears at most once in the list.
                        If an integer appears multiple times, the probabilities are
                        summed in the return value.

    sum_rv():           returns RV obtained by summing two RVs

    die_rv():           returns RV for rolling N dice with M faces.

    keep_high_rv():     returns RV for rolling N dice with M faces, keeping highest K.
    
    sum_mrv_rv():

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

    cartesian_product_mrv():  takes an MRV and an RV and returns a new MRV
                              by performing a Cartesian produt.
    
