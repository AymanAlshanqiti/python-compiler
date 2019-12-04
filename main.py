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
  SymbolTokenHandler({
      '+': [{'+': 'plus'}, {'+':'plusplus'}],
      '-': [{'-': 'minus'}, {'-':'minusminus'}],
      '!': [{'!': 'not'}, {'=': 'notequal'}, {'=': 'noteqeq'}],
      ';': [{';': 'semicolon'}],
      '=': [{'=': 'assignment'}, {'=':'eqeq'}],
      '(': [{'(': 'left_paren'}],
      ')': [{')': 'right_paren'}]
    }),
  StringTokenHandler(),
])

prs = Parser(tk, [PrintStatementParser()])
print(prs.parse())
# for token in tk:
#   print(token.category, '->', token.type, '->', token.value)