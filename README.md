# Overview

Generate random numbers using dice notation.

# How to Run

    $ pip install virtualenv

    $ make ve

    $ ./root.sh 3d6
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

If the code is run in template mode, only expressions inside double
square brackets are interpreted as dice notation:

    Str: \[\[3d6\]\] Int: \[\[3d6]] Wis: \[\[3d6]]
    Dex: \[\[3d6\]\] Con: \[\[3d6]] Cha: \[\[3d6]]

Dice noation can be escaped.

Double square brackets can be used outside of template mode to nest
expressions. For example, to roll a random number of sixers and sum
them:

    \[\[d6\]\]d6

Roll 4 sixers and keep the highest 3:

    4d6k3
    
Equivalently, roll 4 sixers and drop the lowest:

    4d6d1

It is possible to be explicit about whether high or low dice are kept or dropped:

    4d6kh3
    4d6kl3
    4d6dl1
    436dh1

Re-rolls.

Simulate a d7 by rolling a d8, re-rerolling on 1:

    d8r-1
    
Equivalently, simulate a d7 by rolling a d8, re-rolling on 8:

    d8r8
    
Equivalently, simulate a d7 by rolling a d10, re-rolling on 8 or higher:

    d10r>7

Exploding dice:

    d6!
    
Exploding dice with extra-roll condition:

    d6!>3

Hackmaster-style (aka penetrating exploding dice):

    d6!p

Arithmetic operators:

    + - * / %

round(), floor(), ceil(), abs()

# TODO

* set seed
