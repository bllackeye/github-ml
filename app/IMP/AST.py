# Abstract Syntax Tree.

from app.IMP.equality import *


'''An arithmetic expression can take one of three forms:

Literal integer constants, such as 42
Variables, such as x
Binary operations, such as x + 42. These are made out of other arithmetic expressions.
'''

# An Arithmetic Expression;
class Aexp(Equality):
    pass
# Literal Integer
class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

# Integer variable
class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarAexp(%s)' % self.name
# Binary Expression
class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.op, self.left, self.right)


'''
There are four kinds of Boolean expressions.

1) Relational expressions (such as x < 10)
2) And expressions (such as x < 10 and y > 20)
3) Or expressions
4) Not expressions
'''

class Bexp(Equality):
    pass

class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op=op
        self.left=left
        self.right=right
    def __repr__(self):
        return 'RelopBexp(%s, %s, %s)' % (self.op, self.left, self.right)

class AndBexp(Bexp):
    def __init__(self, left, right):
       self.left=left
       self.right=right
    def __repr__(self):
        return 'AndBexp( %s, %s)' % (self.left, self.right)
class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left=left
        self.right=right

    def __repr__(self):
        return 'OrBexp( %s, %s)' % (self.left, self.right)

class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp=exp

    def __repr__(self):
        return 'NotBexp( %s)' % (self.exp)


'''
Statements can contain both arithmetic and Boolean expressions.
There are four kinds of statements:
1) assignment,
2) compound,
3) conditional,
4) and loop.
'''

class Statement(Equality):
    pass
# variable := arithematic expression;
class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name=name
        self.aexp=aexp
    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.aexp)


# statement 1; statement2 ;
class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first=first
        self.second=second
    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

# if condition then
class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition=condition
        self.true_stmt=true_stmt
        self.false_stmt=false_stmt

    def __repr__(self):
        return 'IfStatement(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition=condition
        self.body=body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)