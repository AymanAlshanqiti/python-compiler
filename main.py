from lex.tokenizer import *
from lex.handler import *
from lex.token import *
from lex.handlers.number import NumberTokenHandler
from lex.handlers.whitespace import WhitespaceTokenHandler
from lex.handlers.identifier import IdentifierTokenHandler
from lex.handlers.comment import CommentTokenHandler
from lex.handlers.symbol import SymbolTokenHandler
from lex.handlers.string import StringTokenHandler

from parser.parser import *
from parser.statements.print import PrintStatementParser

with open('main.stp', 'r') as ay:
  code = ay.read(1024)

tk = Tokenizer(code,[
  WhitespaceTokenHandler(),
  NumberTokenHandler(),
  IdentifierTokenHandler(['var', 'let', 'print', 'if', 'else', 'end', 'for','while', 'int', 'float', 'boolean', 'string'],{
    'false': 'boolean',
    'true': 'boolean',
    'null': 'null',
    'nil': 'null',
    'none': 'null'
  }),
  CommentTokenHandler(),
  SymbolTokenHandler( {
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

# for token in tk:
#   print(token.category, '->', token.type, '->', token.value)