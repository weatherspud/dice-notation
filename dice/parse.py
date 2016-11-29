# pylint: disable=pointless-statement
# pylint: disable=expression-not-assigned
import sys

import pyparsing

import dice.const as const

digit = pyparsing.Regex(r'([1-9]\d*)')
digit.setParseAction(lambda toks: (const.OP_LITERAL, int(toks[0])))

single_die_expr = pyparsing.Literal('d') + digit
single_die_expr.setParseAction(lambda toks: (const.OP_DIE, (const.OP_LITERAL, 1), toks[1]))

multiple_die_expr = digit + pyparsing.Literal('d') + digit
multiple_die_expr.setParseAction(lambda toks: (const.OP_DIE, toks[0], toks[2]))


def process_keep_drop_expr(toks: tuple) -> tuple:
    if toks[4] > toks[0]:
        raise Exception('cannot keep or drop more dice than are rolled')
    if toks[3] == 'k' or toks[3] == 'kh':
        return (const.OP_KEEP_HIGH, toks[0], toks[2], toks[4])
    if toks[3] == 'kl':
        return (const.OP_KEEP_LOW, toks[0], toks[2], toks[4])
    elif toks[3] == 'd' or toks[3] == 'dl':
        return (const.OP_KEEP_HIGH, toks[0], toks[2], (const.OP_LITERAL, toks[0][1] - toks[4][1]))
    elif toks[3] == 'dh':
        return (const.OP_KEEP_LOW, toks[0], toks[2], (const.OP_LITERAL, toks[0][1] - toks[4][1]))
    else:
        raise Exception('unrecognized keep/drop operator: {}'.format(toks[3]))

keep_drop_op = pyparsing.Regex(r'kh|kl|dh|dl|k|d')
keep_drop_expr = digit + pyparsing.Literal('d') + digit + keep_drop_op + digit
keep_drop_expr.setParseAction(process_keep_drop_expr)

int_expr = keep_drop_expr | multiple_die_expr | single_die_expr | digit


def process_prod_expr(toks: tuple) -> tuple:
    if len(toks) == 1:
        return toks[0]
    op = const.OP_MULTIPLY if toks[1] == '*' else '/'
    if len(toks) == 3:
        return (op, toks[0], toks[2])
    else:
        return (op, toks[0], process_prod_expr(toks[2:]))

prod_rest_expr = pyparsing.Word('*/', max=1) + int_expr
prod_expr = int_expr + pyparsing.ZeroOrMore(prod_rest_expr)
prod_expr.setParseAction(process_prod_expr)


def process_sum_expr(toks: tuple) -> tuple:
    if len(toks) == 1:
        return toks[0]
    op = const.OP_ADD if toks[1] == '+' else const.OP_SUBTRACT
    if len(toks) == 3:
        return (op, toks[0], toks[2])
    else:
        return (op, toks[0], process_sum_expr(toks[2:]))

sum_rest_expr = pyparsing.Word('+-', max=1) + prod_expr
sum_expr = prod_expr + pyparsing.ZeroOrMore(sum_rest_expr)
sum_expr.setParseAction(process_sum_expr)


def parse(expr: str) -> tuple:
    try:
        return sum_expr.parseString(expr, parseAll=True)[0]
    except pyparsing.ParseException as e:
        sys.stderr.write('PARSE ERROR: input: {} error: {}\n'.format(expr, str(e)))
        raise
