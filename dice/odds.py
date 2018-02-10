#!/usr/bin/env python
from fractions import Fraction
import itertools
import operator
import sys
from typing import Iterable, List, Optional, Tuple

import dice.const as const
import dice.parse as parse

ProbabilityFraction = Fraction
ProbabilityFloat = float
Probability = ProbabilityFloat
# pylint: disable=invalid-sequence-index
RV = List[Tuple[int, Probability]]
IterRV = Iterable[Tuple[int, Probability]]
MRV = List[Tuple[List[int], Probability]]
IterMRV = Iterable[Tuple[List[int], Probability]]
EGF = List[Tuple[int, Probability]]


def probability_fraction(numer: int, denom: int=1) -> Fraction:
    return Fraction(numer, denom)


def probability_float(numer: int, denom: int=1) -> float:
    return numer * 1.0 / denom

probability = probability_float


def eval_literal(ast: tuple) -> int:
    if ast[0] == const.OP_LITERAL:
        return ast[1]
    else:
        raise Exception('unsupported operation: {}'.format(ast[0]))


def dedupe_rv(rv: IterRV) -> RV:
    _rv = list(rv)
    return [(i, sum(pair[1] for pair in pairs))
            for i, pairs
            in itertools.groupby(sorted(_rv, key=operator.itemgetter(0)),
                                 key=operator.itemgetter(0))]


def empty_to_none(iterable: IterRV) -> Optional[IterRV]:
    if isinstance(iterable, list):
        if len(iterable) == 0:
            return None
        else:
            return iterable
    try:
        first = next(iterable)  # type: ignore
    except StopIteration:
        return None
    return itertools.chain([first], iterable)


def sum_rv(rv1: IterRV, rv2: IterRV) -> RV:
    _rv1 = empty_to_none(rv1)
    _rv2 = empty_to_none(rv2)
    if _rv1 is None:
        if _rv2 is None:
            raise Exception('cannot sum two empty lists')
        else:
            return dedupe_rv(_rv2)
    else:
        if _rv2 is None:
            return dedupe_rv(_rv1)
        else:
            return dedupe_rv((i1 + i2, p1 * p2)
                             for (i1, p1)
                             in _rv1
                             for (i2, p2)
                             in _rv2)


def multiply_scalar_rv(rv: IterRV, scalar: int) -> RV:
    return [(i * scalar, p) for i, p in rv]


def _die_rv(num_dice: int, num_faces: int, accum: RV) -> RV:
    assert(0 <= num_dice < const.MAX_NUM_DICE_ODDS)
    if num_dice == 0:
        return accum
    else:
        return _die_rv(num_dice - 1,
                       num_faces,
                       sum_rv(((i, probability(1, num_faces))
                               for i
                               in range(1, num_faces + 1)),
                              accum))


def die_rv(num_dice: int, num_faces: int) -> RV:
    return _die_rv(num_dice, num_faces, [])


def dedupe_mrv(mrv: IterMRV) -> MRV:
    _mrv = list(mrv)
    return [(a, sum(pair[1] for pair in pairs))
            for a, pairs
            in itertools.groupby(sorted(_mrv, key=operator.itemgetter(0)),
                                 key=operator.itemgetter(0))]


def tail_mrv(mrv: MRV, list_len: int) -> MRV:
    return [(a[-list_len:], p) for a, p in mrv]


def sorted_mrv(mrv: MRV) -> MRV:
    return [(sorted(a), p) for a, p in mrv]


def sum_mrv_rv(mrv: IterMRV) -> RV:
    return dedupe_rv((sum(rolls), prob) for rolls, prob in mrv)


def cartesian_product_mrv(mrv: IterMRV, rv: IterRV) -> MRV:
    _rv = list(rv)
    retval = [(a + [o], p1 * p2) for a, p1 in mrv for o, p2 in _rv]

    return retval


def keep_high_rv(num_dice: int,
                 num_faces: int,
                 num_keep: int) -> RV:

    def _keep_high_rv(mrv: IterMRV, num_keep: int) -> IterMRV:
        return ((list(reversed(sorted(a)))[:num_keep], p) for a, p in mrv)

    def _list_odds(num_dice: int, num_faces: int, accum: MRV) -> MRV:
        assert(0 <= num_dice < const.MAX_NUM_DICE_ODDS)
        if num_dice == 0:
            return accum
        elif len(accum) == 0:
            if num_dice == 1:
                return [([i], probability(1, num_faces))
                        for i
                        in range(1, num_faces + 1)]
            else:
                return _list_odds(num_dice - 2,
                                  num_faces,
                                  cartesian_product_mrv([([i], probability(1, num_faces))
                                                         for i
                                                         in range(1, num_faces + 1)],
                                                        [(i, probability(1, num_faces))
                                                         for i
                                                         in range(1, num_faces + 1)]))
        else:
            return _list_odds(num_dice - 1,
                              num_faces,
                              cartesian_product_mrv(accum,
                                                    [(i, probability(1, num_faces))
                                                     for i
                                                     in range(1, num_faces + 1)]))

    return sum_mrv_rv(_keep_high_rv(_list_odds(num_dice, num_faces, []), num_keep))


def keep_low_rv(num_dice: int,
                num_faces: int,
                num_keep: int) -> RV:

    def _keep_low_rv(mrv: IterMRV, num_keep: int) -> IterMRV:
        return ((list(sorted(a))[:num_keep], p) for a, p in mrv)

    def _list_odds(num_dice: int, num_faces: int, accum: MRV) -> MRV:
        assert(0 <= num_dice < const.MAX_NUM_DICE_ODDS)
        if num_dice == 0:
            return accum
        elif len(accum) == 0:
            if num_dice == 1:
                return [([i], probability(1, num_faces))
                        for i
                        in range(1, num_faces + 1)]
            else:
                return _list_odds(num_dice - 2,
                                  num_faces,
                                  cartesian_product_mrv([([i], probability(1, num_faces))
                                                         for i
                                                         in range(1, num_faces + 1)],
                                                        [(i, probability(1, num_faces))
                                                         for i
                                                         in range(1, num_faces + 1)]))
        else:
            return _list_odds(num_dice - 1,
                              num_faces,
                              cartesian_product_mrv(accum,
                                                    [(i, probability(1, num_faces))
                                                     for i
                                                     in range(1, num_faces + 1)]))

    return sum_mrv_rv(_keep_low_rv(_list_odds(num_dice, num_faces, []), num_keep))


def dice_notation_rv(expr: str) -> RV:

    def eval_ast_rv(ast: tuple) -> RV:
        if ast[0] == const.OP_LITERAL:
            return [(ast[1], probability(1))]
        elif ast[0] == const.OP_DIE:
            return die_rv(eval_literal(ast[1]), eval_literal(ast[2]))
        elif ast[0] == const.OP_KEEP_HIGH:
            return keep_high_rv(eval_literal(ast[1]),
                                eval_literal(ast[2]),
                                eval_literal(ast[3]))
        elif ast[0] == const.OP_KEEP_LOW:
            return keep_low_rv(eval_literal(ast[1]),
                               eval_literal(ast[2]),
                               eval_literal(ast[3]))
        elif ast[0] == const.OP_ADD:
            return sum_rv(eval_ast_rv(ast[1]), eval_ast_rv(ast[2]))
        elif ast[0] == const.OP_MULTIPLY:
            if ast[1][0] == const.OP_LITERAL:
                return multiply_scalar_rv(eval_ast_rv(ast[2]), ast[1][1])
            elif ast[2][0] == const.OP_LITERAL:
                return multiply_scalar_rv(eval_ast_rv(ast[1]), ast[2][1])
            else:
                raise Exception('one argument of multiplication must be literal')
        else:
            raise Exception('unsupported operation: {}'.format(ast[0]))

    return eval_ast_rv(parse.parse(expr))


def dice_notation_egf(expr: str) -> EGF:
    retval = []  # type: RV
    cumulative_p = probability(0)
    for i, p in reversed(dice_notation_rv(expr)):
        cumulative_p += p
        retval.append((i, cumulative_p))

    return retval

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('USAGE: odd.py EXPRESSION')
    else:
        cumsum = 0.0
        for i, p in dice_notation_rv(sys.argv[1]):
            if Probability == ProbabilityFraction:
                # pylint: disable=no-member
                print("{}: {}/{}".format(i, p.numerator, p.denominator))  # type: ignore
            else:
                # print("{}: ({}%)".format(i, '%.3f' % (100.0 * p)))
                cumsum += p
                print("{}\t{}\t{}".format(i, '%.4f' % (100.0 * p), '%.4f' % (100.0 * cumsum)))
