#!/usr/bin/env python
from fractions import Fraction
import operator
from typing import List

import dice.classes
import dice.odds as odds

PROB_FMT = '%.3f'


def standard(min_attributes: List[int], roll_expr: str='3d6') -> Fraction:
    score_to_prob_list = odds.dice_notation_egf(roll_expr)
    score_to_prob = {}
    for i, p in score_to_prob_list:
        score_to_prob[i] = p
    prob = Fraction(1)
    for min_attr in min_attributes:
        prob *= score_to_prob[min_attr]

    return prob


def list_greater_or_equal(a1: List[int], a2: List[int]) -> bool:
    for i, x1 in enumerate(a1):
        if x1 < a2[i]:
            return False

    return True


def sorted_attributes(roll_expr: str='3d6') -> None:
    accum = [([o], p) for o, p in odds.dice_notation_rv(roll_expr)]
    for _ in range(1, 6):
        accum = odds.dedupe_mrv(odds.sorted_mrv(
            odds.cartesian_product_mrv(accum,
                                       odds.dice_notation_rv(roll_expr))))
    for _class, min_attributes in sorted(dice.classes.MIN_ATTRIBUTES.items(),
                                         key=operator.itemgetter(0)):
        sorted_min_attributes = sorted(min_attributes)
        cumulative_p = 0.0
        for a, p in accum:
            if list_greater_or_equal(a, sorted_min_attributes):
                cumulative_p += p
        print('{}: ({}%)'.format(_class, PROB_FMT % (100.0 * cumulative_p)))


def best_of(roll_expr: str='3d6', best_of: int=12) -> None:
    assert(best_of >= 6)
    accum = [([o], p) for o, p in odds.dice_notation_rv(roll_expr)]
    for _ in range(1, best_of):
        prod = odds.cartesian_product_mrv(accum, odds.dice_notation_rv(roll_expr))
        sort = odds.sorted_mrv(prod)
        short = odds.tail_mrv(sort, 6)
        dedupe = odds.dedupe_mrv(short)
        accum = dedupe
    for _class, min_attributes in sorted(dice.classes.MIN_ATTRIBUTES.items(),
                                         key=operator.itemgetter(0)):
        sorted_min_attributes = sorted(min_attributes)
        cumulative_p = 0.0
        for a, p in accum:
            if list_greater_or_equal(a[:6], sorted_min_attributes):
                cumulative_p += p
        print('{}: ({}%)'.format(_class, PROB_FMT % (100.0 * cumulative_p)))


def best_of_attribute(roll_expr: str='3d6', best_of: int=6) -> None:
    initial_odds = odds.dice_notation_egf(roll_expr)
    best_of_odds = {}
    for i, p in initial_odds:
        best_of_odds[i] = 1 - (1 - p) ** best_of
    for _class, min_attributes in sorted(dice.classes.MIN_ATTRIBUTES.items(),
                                         key=operator.itemgetter(0)):
        cumulative_p = 1.0
        for attr in min_attributes:
            cumulative_p *= best_of_odds[attr]
        print('{}: ({}%)'.format(_class, PROB_FMT % (100.0 * cumulative_p)))


if __name__ == '__main__':
    print('CHANCES 3d6:')
    for _class, min_attributes in sorted(dice.classes.MIN_ATTRIBUTES.items(),
                                         key=operator.itemgetter(0)):
        p = standard(min_attributes, '3d6')
        try:
            print('{}: {}/{} ({}%)'.format(_class,
                                           p.numerator,
                                           p.denominator,
                                           PROB_FMT % (p * 100.0)))
        except AttributeError:
            print('{}: ({}%)'.format(_class, PROB_FMT % (p * 100.0)))

    print()
    print('CHANCES 4d6k3:')
    for _class, min_attributes in sorted(dice.classes.MIN_ATTRIBUTES.items(),
                                         key=operator.itemgetter(0)):
        p = standard(min_attributes, '4d6k3')
        try:
            print('{}: {}/{} ({}%)'.format(_class,
                                           p.numerator,
                                           p.denominator,
                                           PROB_FMT % (p * 100.0)))
        except AttributeError:
            print('{}: ({}%)'.format(_class, PROB_FMT % (p * 100.0)))

    print()
    print('CHANCES 3d6 PLAYER-ARRANGED:')
    sorted_attributes('3d6')

    print()
    print('(METHOD I) CHANCES 4d6k3 PLAYER-ARRANGED:')
    sorted_attributes('4d6k3')

    print()
    print('(METHOD II) CHANCES 3d6 BEST-OF-12 PLAYER-ARRANGED:')
    best_of('3d6', best_of=12)

    print()
    print('(METHOD III) CHANCES 3d6 BEST-OF-6 EACH ATTRIBUTE:')
    best_of_attribute('3d6', best_of=6)

    print()
    print('(METHOD IV) CHANCES BEST-OF-12-CHARACTERS 3d6:')
    for _class, min_attributes in sorted(dice.classes.MIN_ATTRIBUTES.items(),
                                         key=operator.itemgetter(0)):
        p = standard(min_attributes, '3d6')
        best_of_12_p = 1 - (1 - p) ** 12
        try:
            print('{}: {}/{} ({}%)'.format(_class,
                                           p.numerator,
                                           p.denominator,
                                           PROB_FMT % (best_of_12_p * 100.0)))
        except AttributeError:
            print('{}: ({}%)'.format(_class, PROB_FMT % (best_of_12_p * 100.0)))
