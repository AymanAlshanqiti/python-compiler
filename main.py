from lex.tokenizer import *
from lex.handler import *
from lex.token import *
from lex.handlers.number import NumberTokenHandler


with open('main.stp', 'r') as ay:
  code = ay.read(1024)

for token in TokenizerList(code, [
  NumberTokenHandler()
]).tokens:
  print(token.value)

