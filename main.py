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
from step.syntax.statements.fun import FunStatementParser


with open('main.stp', 'r') as ay:
  code = ay.read(1024)

tk = Tokenizer(code,[
  WhitespaceTokenHandler(True),
  NumberTokenHandler(),
  IdentifierTokenHandler(['fun', 'var', 'let', 'print', 'if', 'else', 'end', 'for','while', 'int', 'float', 'boolean', 'string'],{
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
      ')': [{')': 'right_paren'}],
      ',': [{',': 'comma'}]
    }),
  StringTokenHandler(),
])


def expand_symt(symt, level = 1):
  print((' ' * level) + '@' + symt.name)
  for name, entry in symt.entries.items():
    if entry.type == 'var':
      print((' ' * level) + '#' + entry.name)
    elif entry.type == 'parameter':
      print((' ' * level) + '[]' + entry.name)
    elif entry.type == 'fun':
      print((' ' * level) + '{\}' + entry.name)
      expand_symt(entry.attributes['symt'], level + 2)

gsymt = SymbolTable('global')
prs = Parser(tk, gsymt, [PrintStatementParser(), VarStatementParser(), WhileStatementParser(), EndStatementParser(), FunStatementParser()])
statements = prs.statement()
expand_symt(gsymt)
