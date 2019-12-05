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
    }),
  SymbolTokenHandler('punctuation', {
      ';': [{';': 'semicolon'}],
      '(': [{'(': 'left_paren'}],
      ')': [{')': 'right_paren'}]
    }),
  StringTokenHandler(),
])

# for token in tk:
#   print(token.category, '->', token.type, '->', token.value)

prs = Parser(tk, [PrintStatementParser(), VarStatementParser(), WhileStatementParser()])
statements = prs.statement()
print(statements)
