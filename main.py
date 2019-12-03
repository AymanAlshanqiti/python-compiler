from lex.tokenizer import *
from lex.handler import *
from lex.token import *
from lex.handlers.number import NumberTokenHandler
from lex.handlers.whitespace import WhitespaceTokenHandler
from lex.handlers.identifier import IdentifierTokenHandler
from lex.handlers.comment import CommentTokenHandler

with open('main.stp', 'r') as ay:
  code = ay.read(1024)

tk = Tokenizer(code,[
  WhitespaceTokenHandler(),
  NumberTokenHandler(),
  IdentifierTokenHandler(['var', 'let', 'print', 'if', 'else', 'end', 'for'],{
    'false': 'boolean',
    'true': 'boolean',
    'null': 'null'
  }),
  CommentTokenHandler()
])

for token in tk:
  print(token.category, '->', token.type, '->', token.value)