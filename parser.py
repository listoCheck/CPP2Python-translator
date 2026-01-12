from lexer import Token
from ast_nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def cur(self):
        return self.tokens[self.pos]

    def eat(self, tp):
        if self.cur().type == tp:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {tp}, got {self.cur()}")

    def parse(self):
        res = []
        while self.cur().type != 'EOF':
            res.append(self.item())
        return Program(res)

    def item(self):
        t = self.cur().type
        if t == 'CLASS':
            return self.class_decl()
        if t == 'INT':
            return self.func_or_var()
        if t == 'IDENT':
            return self.assignment()
        if t == 'IF':
            return self.if_stmt()
        if t == 'WHILE':
            return self.while_stmt()
        if t == 'RETURN':
            return self.return_stmt()
        if t in ('CIN', 'COUT'):
            return self.io_stmt()
        if t in ('LINE_COMMENT', 'BLOCK_COMMENT'):
            comment_text = self.cur().value
            self.eat(t)
            return Comment(comment_text)
        raise SyntaxError(f"Invalid statement at {self.cur()}")

    def class_decl(self):
        self.eat('CLASS')
        name = self.cur().value
        self.eat('IDENT')
        self.eat('LBRACE')
        members = []
        while self.cur().type != 'RBRACE':
            members.append(self.item())
        self.eat('RBRACE')
        return Class(name, members)

    def func_or_var(self):
        self.eat('INT')
        name = self.cur().value
        self.eat('IDENT')
        if self.cur().type == 'LPAREN':  # функция
            return self.function(name)
        elif self.cur().type == 'ASSIGN':  # переменная с инициализацией
            self.eat('ASSIGN')
            expr = self.expr()
            self.eat('SEMICOLON')
            return Assign(name, expr)
        elif self.cur().type == 'SEMICOLON':  # переменная без инициализации
            self.eat('SEMICOLON')
            return Assign(name, None)
        else:
            raise SyntaxError(f"Expected ASSIGN or SEMICOLON, got {self.cur()}")

    def function(self, name):
        self.eat('LPAREN')
        params = []
        if self.cur().type != 'RPAREN':
            while True:
                self.eat('INT')
                param_name = self.cur().value
                self.eat('IDENT')
                params.append(param_name)
                if self.cur().type == 'COMMA':
                    self.eat('COMMA')
                else:
                    break
        self.eat('RPAREN')
        body = self.block()
        return Func(name, params, body)

    def assignment(self):
        name = self.cur().value
        self.eat('IDENT')
        self.eat('ASSIGN')
        expr = self.expr()
        self.eat('SEMICOLON')
        return Assign(name, expr)

    def if_stmt(self):
        self.eat('IF')
        self.eat('LPAREN')
        cond = self.expr()
        self.eat('RPAREN')
        body = self.block()
        return If(cond, body)

    def while_stmt(self):
        self.eat('WHILE')
        self.eat('LPAREN')
        cond = self.expr()
        self.eat('RPAREN')
        body = self.block()
        return While(cond, body)

    def return_stmt(self):
        self.eat('RETURN')
        expr = self.expr()
        self.eat('SEMICOLON')
        return Return(expr)

    def io_stmt(self):
        t = self.cur().type
        if t == 'CIN':
            self.eat('CIN')
            vars_ = []
            self.eat('SHR')
            vars_.append(self.cur().value)
            self.eat('IDENT')
            while self.cur().type == 'SHR':
                self.eat('SHR')
                vars_.append(self.cur().value)
                self.eat('IDENT')
            self.eat('SEMICOLON')
            return Cin(vars_)
        else:  # COUT
            self.eat('COUT')
            outputs = []
            self.eat('SHL')
            outputs.append(self.expr())
            while self.cur().type == 'SHL':
                self.eat('SHL')
                outputs.append(self.expr())
            self.eat('SEMICOLON')
            return Cout(outputs)

    def block(self):
        self.eat('LBRACE')
        stmts = []
        while self.cur().type != 'RBRACE':
            stmts.append(self.item())
        self.eat('RBRACE')
        return stmts

    def expr(self):
        node = self.term()
        while self.cur().type in ('PLUS', 'MINUS'):
            op = self.cur().value
            self.eat(self.cur().type)
            node = BinOp(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.cur().type in ('MUL', 'DIV'):
            op = self.cur().value
            self.eat(self.cur().type)
            node = BinOp(node, op, self.factor())
        return node

    def factor(self):
        tok = self.cur()
        if tok.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(tok.value)
        if tok.type == 'IDENT':
            name = tok.value
            self.eat('IDENT')
            if self.cur().type == 'LPAREN':  # вызов функции
                self.eat('LPAREN')
                args = []
                if self.cur().type != 'RPAREN':
                    while True:
                        args.append(self.expr())
                        if self.cur().type == 'COMMA':
                            self.eat('COMMA')
                        else:
                            break
                self.eat('RPAREN')
                return FuncCall(name, args)
            return Variable(name)
        if tok.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        raise SyntaxError(f"Invalid expression at {tok}")
