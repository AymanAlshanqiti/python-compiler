from lex.handler import TokenHandler
from lex.token import Token


class WhitespaceTokenHandler(TokenHandler):

  def is_tokenizable(self, tokenizer):
    return tokenizer.peek.isspace()

  def tokenize(self, tokenizer):
    token = Token('space', 'space')
    token.value = tokenizer.next_character
    token.position = tokenizer.position
    token.line_number = tokenizer.line_number

    if tokenizer.character == '\n':
      tokenizer.line_number += 1
    
    while not tokenizer.is_eof and tokenizer.peek.isspace():
      token.value += tokenizer.next_character
      if tokenizer.character == '\n':
        tokenizer.line_number += 1
    return token