# --- Code to parse a function object from a given string --- #

from Expressions import *


# string keys for unary functions (1 input)
UNOPS = {'ln': Natural_log, 'sin': Sine, 'cos': Cosine, 'arcsin': Arcsin}

# string keys for binary functions (2 inputs)
BINOPS = {'+': Addition, '*': Multiplication, '^': Power}


# takes a function string and returns a function object
# builds function object tree recursively
def parse_func(string):
    string = string.replace(' ', '')

    if string[0] == '(' and string[-1] == ')' and parens_balanced(string[1:-1]):
        string = string[1:-1]

    if string.isdigit() or (string[0] == '-' and string[1:].isdigit()):
        return Constant(int(string))

    if len(string) == 1:
        return Var(string)

    opens = 0
    for i in range(len(string) - 2):
        if string[i] == '(':
            opens += 1
        elif string[i] == ')':
            opens -= 1
        if opens == 0:
            char = string[i + 1]
            if char in BINOPS.keys():
                op = BINOPS[char]
                return op(parse_func(string[:i+1]), parse_func(string[i+2:]))

    for key in UNOPS.keys():
        if string.startswith(key):
            return UNOPS[key](parse_func(string[len(key):]))


def parens_balanced(string):
    opens = 0
    for c in string:
        if c == '(':
            opens += 1
        elif c == ')':
            opens -= 1
        if opens < 0: return False
    return opens == 0
