#!/usr/bin/env python
import random
import sys

import dice.const as const
import dice.parse as parse


def eval_int(ast: tuple) -> int:
    if ast[0] == const.OP_LITERAL:
        return ast[1]
    elif ast[0] == const.OP_DIE:
        return sum([random.randint(1, eval_int(ast[2]))
                    for _
                    in range(0, eval_int(ast[1]))])
    elif ast[0] == const.OP_KEEP_HIGH:
        return sum(list(reversed(sorted([random.randint(1, eval_int(ast[2]))
                                         for _
                                         in range(0, eval_int(ast[1]))])))[:eval_int(ast[3])])
    elif ast[0] == const.OP_KEEP_LOW:
        return sum(list(sorted([random.randint(1, eval_int(ast[2]))
                                for _
                                in range(0, eval_int(ast[1]))]))[:eval_int(ast[3])])
    elif ast[0] == const.OP_ADD:
        return eval_int(ast[1]) + eval_int(ast[2])
    elif ast[0] == const.OP_SUBTRACT:
        return eval_int(ast[1]) - eval_int(ast[2])
    elif ast[0] == const.OP_MULTIPLY:
        return eval_int(ast[1]) * eval_int(ast[2])
    else:
        raise Exception('unsupported operation: {}'.format(ast[0]))


def roll(expr: str) -> int:
    return eval_int(parse.parse(expr))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('USAGE: roll.py EXPRESSION')
    else:
        print(roll(sys.argv[1]))
