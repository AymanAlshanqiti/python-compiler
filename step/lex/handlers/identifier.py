from step.lex.token import Token
from step.lex.handler import *
class IdentifierTokenHandler(TokenHandler):

  def __init__(self, keywords=[], literals={}):
    super().__init__()
    self.keywords = keywords
    self.literals = literals

  def is_tokenizable(self, tokenizer):
    return tokenizer.peek().isalpha() or tokenizer.peek() == '_'

  def tokenize(self, tokenizer):
    token = tokenizer.build_token('id','id', lambda t : t.peek().isalnum() or t.peek() == '_')
    
    if token.value in self.keywords:
      token.category = 'keyword'
      token.type = 'keyword'
    
    if token.value in self.literals.keys():
      token.category = 'literal'
      token.type = self.literals[token.value]

    return token