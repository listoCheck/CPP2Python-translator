class Program:
    def __init__(self, statements):
        self.statements = statements


class Assign:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class If:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class While:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Number:
    def __init__(self, value):
        self.value = value


class Variable:
    def __init__(self, name):
        self.name = name


class Return:
    def __init__(self, expr):
        self.expr = expr


class Cin:
    def __init__(self, vars_):
        self.vars = vars_


class Cout:
    def __init__(self, outputs):
        self.outputs = outputs


class Func:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class FuncCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args


class Class:
    def __init__(self, name, members):
        self.name = name
        self.members = members


class Comment:
    def __init__(self, text):
        self.text = text
