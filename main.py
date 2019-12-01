from tokenizer import Tokenizer, TokenizerList
from token import Token
from token_handler import *
from parser import *


with open('code.ay', 'r') as ay:
  code = ay.read(1024)


parser = Parser(TokenizerList(code, ay_tokenizer_handlers))
program = parser.parse()

if parser.has_error():
  if parser.current_level < 0:
    parser.syntax_error("unexpected end", parser.token.line_number, parser.token.position)
  elif parser.current_level > 0:
    parser.syntax_error("end expected", parser.token.line_number, parser.token.position)


def print_statements(statements, level=1):
  for statement in statements:
    print(level * '\t', end='')
    print("-> statement type: " + statement.type)
    if isinstance(statement, BlockStatement):
      print_statements(statement.statements, level + 1)
    elif isinstance(statement, PrintStatement):
      print_expression(statement.expression)
    elif isinstance(statement, VarStatement):
      print_expression(statement.expression)
    elif isinstance(statement, ForStatement):
      print_expression(statement.from_expression)
      print_expression(statement.to_expression)

    print("-----------------------------------------")

def print_expression(expression, level= 1):
  if isinstance(expression, BinaryExpression):
    print(expression.operator.value)
    print_expression(expression.left_expression, level + 1)
    print_expression(expression.right_expression, level + 1)
  elif isinstance(expression, LiteralExpression):
    print(level * '\t', end='')
    print(expression.value)
  elif isinstance(expression, IdentifierExpression):
    print(level * '\t', end='')
    print(expression.identifier)
  

#print_statements(program)

