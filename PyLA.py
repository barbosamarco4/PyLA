class Value():
    pass

class Set( Value ):
    def __init__(self,values):
        self.values = values
class Function( Value ):
    def Except(self,pos,value):
        return (pos,value)
class Tuple( Value ):
    def __init__(self,value):
        self.value = value

class Literal:
    def __init__(self,value):
        self.value = value

class Symbol:
    def __init__(self,name,value):
        self.name = name
        #será que quero permitir isto? não garante uso correto do construtor
        #if isinstance(value,Value):
        #    self.value = value
        if isinstance(value,list) or isinstance(value,tuple):
            self.value = Tuple(value)
        if isinstance(value,dict):
            self.value = Function(value)
        if isinstance(value,set):
            self.value = Set(value)
        if isinstance(value,int) or isinstance(value,str):
            self.value = value
    def __str__(self):
        return self.name
    #TODO: check if other is Conjunction
    def __eq__(self,other):
        return BinaryPredicate(self,'=',other)
    def __ne__(self,other):
        return BinaryPredicate(self,'#',other)
    def __lt__(self,other):
        return BinaryPredicate(self,'<',other)
    def __le__(self,other):
        return BinaryPredicate(self,'<=',other)
    def __gt__(self,other):
        return BinaryPredicate(self,'>', other)
    def __ge__(self,other):
        return BinaryPredicate(self,'>=', other)

    def __add__(self,other):
        return Expr(self,'+',other)
    def __sub__(self,other):
        return Expr(self,'-',other)
    def __mul__(self,other):
        return Expr(self,'*',other)
    #TODO: check if vars are bool
    def __and__(self,other):
        return Conjunction(self,other)
    def __or__(self,other):
        return Disjunction(self,other)
    #TODO: index by expression, multiple indexation
    def __getitem__(self,key):
        return Expr(self,'[]',key)
class Constant( Symbol ):
    pass

class Variable ( Symbol ):
    def __init__(self,name,value):
        super().__init__(name,value)
        self.next = f'{name}\'' 
    def __invert__(self):
        return UnaryPredicate('~',self.name)

class Expr:
    def __init__(self,lhs,op,rhs): 
        self.lhs = lhs
        self.op  = op
        self.rhs = rhs

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
        return str(self.rhs) + self.op + str(self.lhs)

class Formula:
    #formulas because they can be a predicate or a formula
    def __init__(self,a1,a2):
        self.formulas = [a1,a2]

    def __str__(self):
        return str(self.formulas)
    def __and__(self,other):
        if isinstance(other,Predicate):
            self.formulas.append(other)
            return self
        if isinstance(other,Formula):
            return Conjunction(self,other)
        if isinstance(other,Variable):
            return Conjunction(self,UnaryPredicate('',other))
    def __or__(self,other):
        if isinstance(other,Variable):
            self.formulas.append(UnaryPredicate('',other))
            return self
        if isinstance(other,Predicate):
            self.formulas.append(other)
            return self
        if isinstance(other,Formula):
            return Conjunction(self,other)
    
class Conjunction( Formula ):
    def print(self,tabs=''):
        for f in self.formulas:
            if isinstance(f,Formula):
                f.print(tabs+'\t')
            else:
                print(f'{tabs}/\{f}')
class Disjunction( Formula ):
    def print(self,tabs=''):
        for f in self.formulas:
            if isinstance(f,Formula):
                f.print(tabs+'\t')
            else:
                print(f'{tabs}\/{f}')

class Step:
    def __init__(self,name,formula):
         self.name = name
         self.formula = formula

class Definition:
    #example: Messages == {x \in 1..10 | x % 2 = 0}
    pass

class TLA:
    def __init__(self):
        self.constants = { }
        self.variables = set ()
        self.steps = []
