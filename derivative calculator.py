from sympy import simplify



# parent class for all functions (unary and binary)
class Function:
    inputs = 0
    def to_string(self, parens):        # is overridden
        return ""
    def __repr__(self):
        parens = True
        return self.to_string(parens) if self.inputs == 1 else self.to_string(parens)[1:-1]
    def simplified(self):
        return self
    def cheat_simplified(self):
        return simplify(self.to_string(True))
    def equals(self, other):
        return self.to_string(True) == other.to_string(True)




# represents functional constants
class Constant(Function):
    inputs = 1
    def __init__(self, n):
        self.n = n
    def get_derivative(self):
        return Constant(0)
    def to_string(self, parens = False):
        string = str(self.n)
        return string
        # return "(" + string + ")" if parens else string


# represents variable being differentiated with respect to
class Var(Function):
    inputs = 1
    def __init__(self, name):
        self.name = name
    def get_derivative(self):
        return Constant(1)
    def to_string(self, parens = False):
        string = self.name
        return string
        # return "(" + string + ")" if parens else string


# represents the natural logarithm of the 1 given input
class Natural_log(Function):
    inputs = 1
    def __init__(self, n):
        self.n = n
    def get_derivative(self):
        return Multiplication(Power(self.n, Constant(-1)), self.n.get_derivative())
    def to_string(self, parens = False):
        string = "ln(" + self.n.to_string(parens) + ")"
        return string
        # return "(" + string + ")" if parens else string


# represents the sine of the 1 given input
class Sine(Function):
    inputs = 1
    def __init__(self, n):
        self.n = n
    def get_derivative(self):
        return Multiplication(Cosine(self.n), self.n.get_derivative())
    def to_string(self, parens):
        string = "sin(" + self.n.to_string(parens) + ")"
        return string
        # return "(" + string + ")" if parens else string


# represents the cosine of the 1 given input
class Cosine(Function):
    inputs = 1
    def __init__(self, n):
        self.n = n
    def get_derivative(self):
        return Multiplication(Multiplication(Sine(self.n), Constant(-1)), self.n.get_derivative)
    def to_string(self, parens):
        string = "cos(" + self.n.to_string(parens) + ")"
        return string
        # return "(" + string + ")" if parens else string


# represents the cosine of the 1 given input
class Arcsin(Function):
    inputs = 1
    def __init__(self, n):
        self.n = n
    def get_derivative(self):
        return Multiplication(
            Power(Addition(Constant(1), Multiplication(Constant(-1), self.n)), Constant(-0.5)),
            self.n.get_derivative()
        )
    def to_string(self, parens):
        string = "arcsin(" + self.n.to_string(parens) + ")"
        return string
        # return "(" + string + ")" if parens else string


# represents the addition of the 2 given inputs
class Addition(Function):
    inputs = 2
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def get_derivative(self):
        return Addition(self.a.get_derivative(), self.b.get_derivative())           # linearity of differentiation operator
    def simplified(self):
        a = self.a.simplified()
        b = self.b.simplified()
        #print a, b, "\n"
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
    def to_string(self, parens = False):
        string = self.a.to_string(parens) + " + " + self.b.to_string(parens)
        return "(" + string + ")" if parens else string


# represents the multplication of the 2 given inputs
class Multiplication(Function):
    inputs = 2
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def get_derivative(self):
        return Addition(Multiplication(self.a, self.b.get_derivative()), Multiplication(self.a.get_derivative(), self.b))          # product rule
    def simplified(self):
        a = self.a.simplified()
        b = self.b.simplified()
        #print a, b, "\n"
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
    def to_string(self, parens = False):
        string = self.a.to_string(parens) + " * " + self.b.to_string(parens)
        return "(" + string + ")" if parens else string


# represents the exponentiation of the 2 given inputs
class Power(Function):
    inputs = 2
    def __init__(self, base, exp):
        self.base = base
        self.exp = exp
    def get_derivative(self):
        if isinstance(self.exp, Constant):
            return Multiplication(self.exp, Power(self.base, Constant(self.exp.n - 1)))        # monomial power rule
        return Multiplication(          # generalized power rule
            Power(self.base, self.exp),
            Addition(
                Multiplication(self.base.get_derivative(), Multiplication(self.exp, Power(self.base, Constant(-1)))),
                Multiplication(self.exp.get_derivative(), Natural_log(self.base))
            )
        )
    def simplified(self):
        base = self.base.simplified()
        exp = self.exp.simplified()
        #print base, exp, "\n"
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
    def to_string(self, parens = False):
        string = self.base.to_string(parens) + " ^ " + self.exp.to_string(parens)
        return "(" + string + ")" if parens else string




# string keys for unary functiona (1 input)
unops = {"ln": Natural_log, "sin": Sine, "cos": Cosine, "arcsin": Arcsin}


# string keys for binary functiona (2 inputs)
biops = {"+": Addition, "*": Multiplication, "^": Power}

# takes a function string and returns a function object
# builds function object tree recursively
def parse_func(string):
    string = string.replace(" ", "")

    if string[0] == "(" and string[-1] == ")":
        string = string[1:-1]

    # print string

    if string.isdigit() or (string[0] == "-" and string[1:].isdigit()):
        # print "Constant found"
        return Constant(int(string))

    if len(string) == 1:
        # print "Var found"
        return Var(string)

    opens = 0
    for i in range(len(string) - 2):
        if string[i] == "(":
            opens += 1
        elif string[i] == ")":
            opens -= 1
        if opens == 0:
            char = string[i + 1]
            if char in biops.keys():
                op = biops[char]
                # print "op: " + str(op)
                return op(parse_func(string[:i+1]), parse_func(string[i+2:]))

    for key in unops.keys():
        if string.startswith(key):
            return unops[key](parse_func(string[len(key):]))









if __name__ == "__main__":
    x = Var("x")

    func_string = "ln(sin(ln(x^(arcsin(x^ln(x))))))"
    func = parse_func(func_string)
    print func
    der = func.get_derivative().cheat_simplified()
    print der


