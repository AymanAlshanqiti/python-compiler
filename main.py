from step.lex.tokenizer import *
from step.lex.handler import *
from step.lex.token import *
from step.lex.handlers.number import NumberTokenHandler
from step.lex.handlers.whitespace import WhitespaceTokenHandler
from step.lex.handlers.identifier import IdentifierTokenHandler
from step.lex.handlers.comment import CommentTokenHandler
from step.lex.handlers.symbol import SymbolTokenHandler
from step.lex.handlers.string import StringTokenHandler

from step.syntax.parser import *
from step.syntax.statements.print import PrintStatementParser
from step.syntax.statements.var import VarStatementParser
from step.syntax.statements._while import WhileStatementParser
from step.syntax.statements.end import EndStatementParser

with open('main.stp', 'r') as ay:
  code = ay.read(1024)

tk = Tokenizer(code,[
  WhitespaceTokenHandler(True),
  NumberTokenHandler(),
  IdentifierTokenHandler(['var', 'let', 'print', 'if', 'else', 'end', 'for','while', 'int', 'float', 'boolean', 'string'],{
    'false': 'boolean',
    'true': 'boolean',
    'null': 'null',
    'nil': 'null',
    'none': 'null'
  }),
  CommentTokenHandler(),
  SymbolTokenHandler('operator', {
      '+': [{'+': 'plus'}, {'=':'plus_assignment'}],
      '-': [{'-': 'minus'}, {'=':'minus_assignment'}],
      '*': [{'*': 'multiplication'}, {'=':'multiplication_assignment'}],
      '/': [{'/': 'division'}, {'=':'division_assignment'}],
      '!': [{'!': 'not'}, {'=': 'notequal'}, {'=': 'noteqeq'}],
      '=': [{'=': 'assignment'}, {'=':'eqeq'}],
      '>': [{'>': 'gt'}, {'=':'gteq'}],
      '<': [{'<': 'lt'}, {'=':'lteq'}],
    }),
  SymbolTokenHandler('punctuation', {
      ';': [{';': 'semicolon'}],
      '(': [{'(': 'left_paren'}],
      ')': [{')': 'right_paren'}]
    }),
  StringTokenHandler(),
])


prs = Parser(tk, [PrintStatementParser(), VarStatementParser(), WhileStatementParser(), EndStatementParser()])
statements = prs.statement()

def excute_expr(exp):
  result = 0
  if isinstance(exp, BinaryExpression):
    op = exp.operator
    left = exp.left_expression
    right = exp.right_expression
    if op.value == '+' :
      result = excute_expr(left) + excute_expr(right)
    elif op.value == '*':
      result = excute_expr(left) * excute_expr(right)
  elif isinstance(exp, UnaryExpression):
    op = exp.operator
    expression = exp.expression
    if op.value == '-':
      result = -1 * excute_expr(expression)
    elif op.value == '!':
      result = not excute_expr(expression)
  elif isinstance(exp, LiteralExpression):
    if exp.value.type =='number':
      result = int(exp.value.value)
  
  return result

result = excute_expr(statements[0].expression)
print (result)