from lex.handler import TokenHandler
from lex.token import Token

class WhitespaceTokenHandler(TokenHandler):

  def is_tokenizable(self, tokenizer):
    return tokenizer.peek().isspace()

  def tokenize(self, tokenizer):
    token = Token('space','space', tokenizer.nxcharacter(), tokenizer.line_number, tokenizer.position)

    if tokenizer.character() == '\n':
      tokenizer.line_number += 1
    
    while tokenizer.is_peekable() and tokenizer.peek().isspace():
      token.value += tokenizer.nxcharacter()
      if tokenizer.character() == '\n':
        tokenizer.line_number += 1
    return token