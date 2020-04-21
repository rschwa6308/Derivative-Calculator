# --- An Expression is the basic symbolic object --- #

# parent class for all functions (unary and binary)
class Expression:
    def __repr__(self):
        paren_settings = get_parens_setting(self, self.inputs)
        formatted_inputs = [
            f'({i})' if p else f'{i}'
            for i, p in zip(self.inputs, paren_settings)
        ]
        return self.template.format(*formatted_inputs)

    def simplified(self):
        return self

    def cheat_simplified(self):
        return simplify(self.to_string(True))

    def equals(self, other):
        return str(self) == str(other)
    
    # TODO: finish these bois
    def __add__(self, other):
        return Addition(self, other)


# represents constants
class Constant(Expression):
    num_inputs = 0

    def __init__(self, n):
        self.n = n
        self.inputs = [self.n]

    def get_derivative(self, var):
        return Constant(0)
    
    def __repr__(self):
        return str(self.n)


# represents variable being differentiated with respect to
class Var(Expression):
    num_inputs = 0

    def __init__(self, name):
        self.name = name

    def get_derivative(self, var):
        return Constant(1) if var.name == self.name else Constant(0)
    
    def __repr__(self):
        return self.name


# unary operation
class Unop(Expression):
    num_inputs = 1


# binary operation
class Binop(Expression):
    num_inputs = 2


# represents the natural logarithm of the 1 given input
class Natural_log(Unop):
    def __init__(self, n):
        self.n = n
        self.inputs = [self.n]

    def get_derivative(self, var):
        return Multiplication(Power(self.n, Constant(-1)), self.n.get_derivative(var))

    def __repr__(self):
        return f'ln({self.n})'


# represents the sine of the 1 given input
class Sine(Unop):
    def __init__(self, n):
        self.n = n
        self.inputs = [self.n]

    def get_derivative(self, var):
        return Multiplication(Cosine(self.n), self.n.get_derivative(var))
    
    def __repr__(self):
        return f'sin({self.n})'


# represents the cosine of the 1 given input
class Cosine(Unop):
    def __init__(self, n):
        self.n = n
        self.inputs = [self.n]

    def get_derivative(self, var):
        return Multiplication(Multiplication(Sine(self.n), Constant(-1)), self.n.get_derivative(var))
    
    def __repr__(self):
        return f'cos({self.n})'


# represents the cosine of the 1 given input
class Arcsin(Unop):
    def __init__(self, n):
        self.n = n
        self.inputs = [self.n]

    def get_derivative(self, var):
        return Multiplication(
            Power(Addition(Constant(1), Multiplication(Constant(-1), self.n)), Constant(-0.5)),
            self.n.get_derivative(var)
        )
    
    def __repr__(self):
        return f'arcsin({self.n})'


# represents the addition of the 2 given inputs
class Addition(Binop):
    parens = True

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.inputs = [self.a, self.b]
        self.template = '{} + {}'

    def get_derivative(self, var):
        return Addition(self.a.get_derivative(var), self.b.get_derivative(var))           # linearity of differentiation operator

    def simplified(self):
        a = self.a.simplified()
        b = self.b.simplified()
        if isinstance(a, Constant) and isinstance(b, Constant):
            return Constant(a.n + b.n)
        elif isinstance(a, Constant):
            if a.n == 0:
                return b
        elif isinstance(b, Constant):
            if b.n == 0:
                return a
        elif isinstance(a, Multiplication) and isinstance(b, Multiplication):
            if a.a.equals(b.a):
                return Multiplication(a.a, Addition(a.b, b.b).simplified())
            elif a.b.equals(b.a):
                return Multiplication(a.b, Addition(a.a, b.b).simplified())
            elif a.a.equals(b.b):
                return Multiplication(a.a, Addition(a.b, b.a).simplified())
            elif a.b.equals(b.b):
                return Multiplication(a.b, Addition(a.a, b.a))
        return Addition(a, b)


# represents the multiplication of the 2 given inputs
class Multiplication(Binop):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.inputs = [self.a, self.b]
        self.template = '{} * {}'

    def get_derivative(self, var):
        return Addition(                # product rule
            Multiplication(self.a, self.b.get_derivative(var)),
            Multiplication(self.a.get_derivative(var), self.b)
        )

    def simplified(self):
        a = self.a.simplified()
        b = self.b.simplified()
        if isinstance(a, Constant) and isinstance(b, Constant):
            return Constant(a.n * b.n)
        elif isinstance(a, Constant):
            if a.n == 0:
                return Constant(0)
            elif a.n == 1:
                return b
        elif isinstance(b, Constant):
            if b.n == 0:
                return Constant(0)
            elif b.n == 1:
                return a
        elif isinstance(a, Power) and isinstance(b, Power):
            if a.base.equals(b.base):
                return Power(a.base, Addition(a.exp, b.exp).simplified())
        return Multiplication(a, b)


# represents the exponentiation of the 2 given inputs
class Power(Binop):
    parens = True

    def __init__(self, base, exp):
        self.base = base
        self.exp = exp
        self.inputs = [self.base, self.exp]
        self.template = '{} ^ {}'

    def get_derivative(self, var):
        if isinstance(self.exp, Constant):
            return Multiplication(                                                              # monomial power rule
                Multiplication(self.exp, Power(self.base, Constant(self.exp.n - 1))),
                self.base.get_derivative(var)
            )
        return Multiplication(                                                                  # generalized power rule
            Power(self.base, self.exp),
            Addition(
                Multiplication(
                    self.base.get_derivative(var),
                    Multiplication(self.exp, Power(self.base, Constant(-1)))
                ),
                Multiplication(self.exp.get_derivative(var), Natural_log(self.base))
            )
        )

    def simplified(self):
        base = self.base.simplified()
        exp = self.exp.simplified()
        if isinstance(base, Constant) and isinstance(exp, Constant):
            return Constant(base.n ** exp.n)
        elif isinstance(base, Constant):
            if base.n == 0:
                return Constant(0)
            elif base.n == 1:
                return Constant(1)
        elif isinstance(exp, Constant):
            if exp.n == 0:
                return Constant(1)
            elif exp.n == 1:
                return base
        return Power(base, exp)


# For each function type, explicitly specify the cases in which parentheses should be put around inputs
#   format for a case is (Type_a, Type_b, ... , Type_z, p) where p \in {0b00, 0b01, 0b10, 0b11} represents paren placement
#   cases listed in decreasing order of precedence
#   default p-value for an unlisted case is 0b00 (no parens)
PARENS_CASES_MAP = {
    Constant: [],
    Var: [],
    Natural_log: [],
    Sine: [],
    Cosine: [],
    Arcsin: [],
    Addition: [
        (Addition, Addition, 0b00),
        (Addition, Binop, 0b01),
        (Binop, Addition, 0b10),
        (Addition, Unop, 0b00),
        (Unop, Addition, 0b00),
        (Binop, Binop, 0b11),
        (Binop, Expression, 0b10),
        (Expression, Binop, 0b01)
    ],
    Multiplication: [
        (Multiplication, Multiplication, 0b00),
        (Multiplication, Binop, 0b01),
        (Binop, Multiplication, 0b10),
        (Multiplication, Unop, 0b00),
        (Unop, Multiplication, 0b00),
        (Binop, Binop, 0b11),
        (Binop, Expression, 0b10),
        (Expression, Binop, 0b01)
    ],
    Power: [
        (Binop, Binop, 0b11),
        (Binop, Expression, 0b10),
        (Expression, Binop, 0b01)
    ]
}


# Takes the parent context (Expression type) and list of inputs
# Returns a list (of length equal to len(inputs)) of paren placement booleans
def get_parens_setting(context, inputs):
    cases = PARENS_CASES_MAP[context.__class__]
    for case in cases:
        if all(isinstance(i, t) for i, t in zip(inputs, case)):
            p = case[-1]
            return [bool((p >> i) & 1) for i in range(len(inputs))][::-1]   # convert int to bool list
    else:
        return [False, False]


# TODO: this is overly complicated and doesn't allow for more dynamic behavior (e.g. using concatenation instead of '*')
#       replace the PARENS_CASES_MAP with a map from contexts to template strings