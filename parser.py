import lang.exprs as e
from lang.interpreter import Interpeter

debug = False

tokens = (
    'VARNAME',
    'NUMBER',
    'PRINT', #FIXME: this should just be a function/part of module
    'STRING',
    'FUNCTION'
    )

# Tokens

literals = ['=', '(', ')', '{', '}']

t_VARNAME = r'\$[a-zA-Z_][a-zA-Z0-9_]*'
t_PRINT = r'print'
t_FUNCTION = r'function'
t_STRING = r'\"([^\\\n]|(\\.))*?\"'
#t_FN = r'[a-zA-Z0-9_-]*'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex(debug=debug)

# Parsing rules

#precedence = (
    #('left','PLUS','MINUS'),
    #('left','TIMES','DIVIDE'),
    #('right','UMINUS'),
    #)

#global things
fn_expr_buffer = []
names = { }

def p_statement_list(p):
    '''statement_list : statement_list statement
               | statement'''

    if len(p) == 2 and p[1]:
       p[0] = e.StatementList()
       stmt = p[1]
       p[0].addStatement(stmt)
    elif len(p) ==3:
       p[0] = p[1]
       if not p[0]: p[0] = e.StatementList()
       if p[2]:
           stat = p[2]
           p[0].addStatement(stat)

def p_statement_print(t):
    'statement : PRINT expression'

    t[0] = e.PrintStmt(t[2])

def p_statement_assign(t):
    '''statement : VARNAME '=' expression'''
    t[0] = e.Assignment(e.Varname(t[1]), t[3])

def p_expression_function_def(t):
    '''expression : FUNCTION '(' ')' '{' statement_list '}' '''
    t[0] = e.FunctionDef(t[5])

def p_expression_varname(t):
    'expression : VARNAME'
    t[0] = e.Varname(t[1])

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = e.Number(t[1])

def p_expression_string(t):
    '''expression : STRING'''
    
    t[0] = e.String(t[1][1:-1])

def p_execute_fn(t):
    '''execute_fn : VARNAME '(' ')' '''
    t[0] = e.FunctionEval(t[1])

def p_statement_execute_fn(t):
    '''statement : execute_fn '''
    t[0] = t[1]

def p_expression_execute_fn(t):
    '''expression : execute_fn '''
    t[0] = t[1]

def p_error(t):
    if t is not None:
        print("Syntax error at '%s', on line %d" % (t.value, t.lexer.lineno))
    else:
        print "Bonkers stuff is happening..." 

import ply.yacc as yacc
parser = yacc.yacc(debug=debug)

with open('first.test') as f:
    data = f.read()
    lexer.input(data)
    parsed = parser.parse(data, lexer=lexer)

    i = Interpeter(parsed)
    i.interpet()

    #for tok in lexer:
        #print tok
    
