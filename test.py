from Expressions import *
from Parsing import parse_func


x = Var('x')
y = Var('y')

func_string = 'ln(sin(ln(x^(arcsin(x^ln(x)))))) + (x ^ y)'
func = parse_func(func_string)
print(func)
der = func.get_derivative(x).simplified()
print(der)


# f = parse_func('ln(sin(ln(x^(arcsin(x^ln(x))))))')
# print(f.__class__)
# print(f)

f = parse_func('x + 2')
print(f)
g = parse_func('x + 5')

print(f + g)