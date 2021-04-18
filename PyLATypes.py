class Int:
    def check(self,value):
        return isinstance(value,int)
class Str:
    def check(self,value):
        return isinstance(value,str)
class Bool:
    def check(self,value):
        return isinstance(value,bool)

class Record:
    def __init__(self,child):
        self.child = child
    def check(self,value):
        return isinstance(value,dict) and all([self.child.check(x) for x in value.values()])

class Tuple:
    def __init__(self,child):
        self.child = child
    def check(self,value):
        return isinstance(value,tuple) #and every position matches 

class Sequence:
    def __init__(self,child):
        self.child = child
    def check(self,value):
        return isinstance(value,list) and all([self.child.check(x) for x in value])
class Set:
    def __init__(self,child):
        self.child = child
    def check(self,value):
        return isinstance(value,set) and all([self.child.check(x) for x in value])

class Function:
    def __init__(self,domain,image):
        self.domain = domain
        self.image  = image
    def check(self,value):
        return
     
def TypeChecker(name,value,valueType):
    if value!=None  and not valueType.check(value):
        raise TypeError(f'Symbol {name} must be an instance of {valueType} and instead is {type(value)}')
