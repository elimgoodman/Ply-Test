class Expr(object):

    def evaluate(self, scope):
        raise NotImplementedError("Unevaluable! in %s" % (self.__class__.__name__))

class StatementList(Expr):

    def __init__(self):
        self.statements = []

    def addStatement(self, stmt):
        self.statements.append(stmt)

    def evaluate(self, scope):
        for stmt in self.statements:
            stmt.evaluate(scope)

    def __repr__(self):
        out = "(STMTS: \n"
        for stmt in self.statements:
            out += "%s\n" % (stmt)
        out += ")"
        return out
    
class PrintStmt(Expr):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "(PRINT %s)" % (self.value)

    def evaluate(self, scope):
        print self.value.evaluate(scope)

class Assignment(Expr):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s = %s" % (self.left, self.right)

    def evaluate(self, scope):
        scope[self.left.name] = self.right.evaluate(scope)

class Varname(Expr):

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def __repr__(self):
        return "(VAR: %s)" % (self.name)

class Number(Expr):

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self.value

    def __repr__(self):
        return "(NUM: %d)" % (self.value)

class String(Expr):

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self.value

    def __repr__(self):
        return "(STR: \"%s\")" % (self.value)

class FunctionPromise(Expr):
    
    def __init__(self, scope, statements):
        self.scope = scope
        self.statements = statements

    def evaluate(self, scope):
      scope.update(self.scope)
      self.statements.evaluate(scope)

class FunctionDef(Expr):

    def __init__(self, statements):
        self.statements = statements
    
    def evaluate(self, scope):
        return FunctionPromise(scope, self.statements)

    def __repr__(self):
        return "(FN: %s)" % (self.statements)

class FunctionEval(Expr):

    def __init__(self, fn_name):
        self.fn_name = fn_name
    
    def evaluate(self, scope):
        return scope[self.fn_name].evaluate(scope)

    def __repr__(self):
        return "(EVAL FN: %s)" % (self.fn_name)
