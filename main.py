from lex.tokenizer import *
from lex.handler import *
from lex.token import *
from lex.handlers.number import NumberTokenHandler
from lex.handlers.whitespace import WhitespaceTokenHandler

with open('main.stp', 'r') as ay:
  code = ay.read(1024)

tk = Tokenizer(code,[
  WhitespaceTokenHandler(),
  NumberTokenHandler(),
])

for token in tk:
  print(token.category, '->', token.position)