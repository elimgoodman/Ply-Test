class Expr(object):

    def execute(self, scope):
        raise NotImplementedError("Unexecutable!")

class StatementList(Expr):

    def __init__(self):
        self.statements = []

    def addStatement(self, stmt):
        self.statements.append(stmt)

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

    def execute(self, scope):
        print self.value

class Assignment(Expr):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s = %s" % (self.left, self.right)

    def execute(self, scope):
        scope[self.left] = self.right

class Varname(Expr):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "(VAR: %s)" % (self.name)

class Number(Expr):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "(NUM: %d)" % (self.value)

class String(Expr):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "(STR: \"%s\")" % (self.value)

class Function(Expr):

    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return "(FN: %s)" % (self.statements)
