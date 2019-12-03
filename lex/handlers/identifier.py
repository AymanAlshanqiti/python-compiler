from lex.handler import TokenHandler
from lex.token import Token

class IdentifierTokenHandler(TokenHandler):
  def __init__(self, keywords=[]):
    self.keywords = keywords

  def is_tokenizable(self, tokenizer):
    return tokenizer.peek().isalpha() or tokenizer.peek() == '_'

  def tokenize(self, tokenizer):
    token = tokenizer.build_token('id','id', lambda t : t.peek().isalnum() or t.peek() == '_')
    if token.value in self.keywords:
      token.type = 'keyword'
    return token