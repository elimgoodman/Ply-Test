tokens = (
    'VARNAME',
    'NUMBER',
    #'PLUS',
    #'MINUS',
    #'TIMES',
    #'DIVIDE',
    'EQUALS',
    'LPAREN','RPAREN', 
    #'FN'
    'PRINT', #FIXME: this should just be a function/part of module
    'STRING'
    )

# Tokens

#t_PLUS    = r'\+'
#t_MINUS   = r'-'
#t_TIMES   = r'\*'
#t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_VARNAME = r'\$[a-zA-Z_][a-zA-Z0-9_]*'
t_PRINT = r'print'
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
lex.lex()

# Parsing rules

#precedence = (
    #('left','PLUS','MINUS'),
    #('left','TIMES','DIVIDE'),
    #('right','UMINUS'),
    #)

#global things
string_buffer = ""
names = { }

def p_statement_print(t):
    'statement : PRINT expression'

    print "[PRINTER] %s" % t[2]

def p_statement_blank_line(t):
    'statement : '
    pass

def p_statement_assign(t):
    'statement : VARNAME EQUALS expression'
    names[t[1]] = t[3]

def p_expression_varname(t):
    'expression : VARNAME'
    t[0] = names[t[1]]

#def p_words(t):
    #'''words : WORD words
            #| WORD'''
    #string_buffer += t[1]

#def p_expression_binop(t):
    #'''expression : expression PLUS expression
                  #| expression MINUS expression
                  #| expression TIMES expression
                  #| expression DIVIDE expression'''
    #if t[2] == '+'  : t[0] = t[1] + t[3]
    #elif t[2] == '-': t[0] = t[1] - t[3]
    #elif t[2] == '*': t[0] = t[1] * t[3]
    #elif t[2] == '/': t[0] = t[1] / t[3]

#def p_expression_uminus(t):
    #'expression : MINUS expression %prec UMINUS'
    #t[0] = -t[2]

#def p_expression_group(t):
    #'expression : LPAREN expression RPAREN'
    #t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_string(t):
    '''expression : STRING'''
    
    t[0] = t[1][1:-1]


#def p_expression_name(t):
    #'expression : NAME'
    #try:
        #t[0] = names[t[1]]
    #except LookupError:
        #print("Undefined name '%s'" % t[1])
        #t[0] = 0

def p_error(t):
    print("Syntax error at '%s', on line %d" % (t.value, t.lexer.lineno))

import ply.yacc as yacc
yacc.yacc()

with open('first.test') as f:
    lines = f.readlines()
    for line in lines:
        yacc.parse(line)
