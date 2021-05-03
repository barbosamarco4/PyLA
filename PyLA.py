from PyLATypes import *

class Value():
    def __init__(self,name,value=None,valueType=None):
        TypeChecker(name,value,valueType)
        self.name      = name
        self.value     = value
        self.valueType = valueType
    
    def next(self):
        return Value(f'{self.name}\'', valueType = self.valueType)
    def __str__(self):
        return self.name

    def __getitem__(self,key):
        if isinstance(self.valueType, (Record,Tuple,Sequence)):
            return Value(f'{self.name}[{key}]',valueType=self.valueType.child)
        elif isinstance(self.valueType, Function):
            return Value(f'{self.name}[{key}]',valueType=self.valueType.image)
        else:
            raise TypeError(f'Can\'t index an instance of {self.valueType}')

    #TODO: check if vars are Int()
    def __eq__(self,other):
        return BinaryPredicate(self,'=',  other)
    def __ne__(self,other):
        return BinaryPredicate(self,'#',  other)
    def __lt__(self,other):
        return BinaryPredicate(self,'<',  other)
    def __le__(self,other):
        return BinaryPredicate(self,'<=', other)
    def __gt__(self,other):
        return BinaryPredicate(self,'>',  other)
    def __ge__(self,other):
        return BinaryPredicate(self,'>=', other)

    def __add__(self,other):
        return Expr(self,'+',other)
    def __sub__(self,other):
        return Expr(self,'-',other)
    def __mul__(self,other):
        return Expr(self,'*',other)

    def __invert__(self):
        return UnaryPredicate('~',self.name)

    #TODO: check if other is Set()
    def is_in(self,other):
        if isinstance(other, range):
            return BinaryPredicate(self,'\in',other)
        elif isinstance(other, Value) and isinstance(other.valueType, Set):
            return BinaryPredicate(self,'\in',other)
    def is_not_in(self,other):
        if isinstance(other, range):
            return BinaryPredicate(self,'\\notin',other)
        elif isinstance(other, Value) and isinstance(other.valueType, Set):
            return BinaryPredicate(self,'\\notin',other)
def Literal(value):
    #TODO: Infer value type
    return Value(str(value))
def ITE(condition, value1, value2):
    # TODO: Infer and compare value1 and value 2
    # TODO: Typecheck arguments?
    return Value(f'IF {condition} THEN {value1} ELSE {value2}')
class Definition:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    
def Expr(lhs,op,rhs): 
    return Value(f'{str(lhs)} {op} {str(rhs)}',valueType=Int())    

class Predicate:
    def __and__(self,other):
        return Conjunction(self,other)
    def __or__(self,other):
        return Disjunction(self,other)

class UnaryPredicate ( Predicate ):
    def __init__(self,op,name):
        self.op = op
        self.name = name
    def __str__(self):
        return self.op + str(self.name)
class BinaryPredicate (Predicate):
    # lhs -> Variable/Const, rhs -> Variable/Const
    def __init__(self,lhs,op,rhs):
        self.lhs = lhs
        self.op  = op
        self.rhs = rhs
    def __str__(self):
        return f'{str(self.lhs)} {self.op} {str(self.rhs)}'

class Formula:
    #formulas because they can be a predicate or a formula
    def __init__(self,a1,a2):
        self.formulas = [a1,a2]

    def __str__(self):
        return str(self.formulas)
    
class Conjunction( Formula ):
    def __and__(self,other):
        if isinstance(other,Predicate):
            self.formulas.append(other)
            return self
        if isinstance(other,Formula):
            return Conjunction(self,other)
        if isinstance(other,Bool):
            return Conjunction(self,UnaryPredicate('',other))
    def __or__(self,other):
        if isinstance(other,Predicate) or isinstance(other,Formula):
            return Disjunction(self,other)
        if isinstance(other,Bool):
            self.formulas.append(UnaryPredicate('',other))
            return self
    def print(self,tabs=''):
        for f in self.formulas:
            if isinstance(f,Formula):
                print('/\\', end='')
                f.print(tabs+'\t')
            else:
                print(f'{tabs}/\ {f}')

class Disjunction( Formula ):
    def __and__(self,other):
        if isinstance(other,Predicate) or isinstance(other,Formula):
            return Conjunction(self,other)
        if isinstance(other,Bool):
            return Conjunction(self,UnaryPredicate('',other))
    def __or__(self,other):
        if isinstance(other,Predicate):
            self.formulas.append(other)
            return self
        if isinstance(other,Formula):
            return Disjunction(self,other)
        if isinstance(other,Bool):
            self.formulas.append(UnaryPredicate('',other))
            return self
    def print(self,tabs=''):
        for f in self.formulas:
            if isinstance(f,Formula):
                print(f'{tabs}\\/', end='')
                f.print(tabs+'\t')
            else:
                print(f'{tabs}\/ {f}')

class Step:
    def __init__(self,name,formula):
         self.name = name
         self.formula = formula
    def print(self):
        print(f'{self.name} ==')
        self.formula.print('\t')

class Definition:
    #example: Messages == {x \in 1..10 | x % 2 = 0}
    def __init__(self,name, expr):
        pass
class TLA:
    def __init__(self):
        self.constants = { }
        self.variables = set ()
        self.definitions = []
    def addStep(self,steps):
        pass
