from lex.handler import TokenHandler
from lex.token import Token

class CommentTokenHandler(TokenHandler):
  def __init__(self, delimiter='#'):
    self.delimiter = delimiter

  def is_tokenizable(self, tokenizer):
    return tokenizer.peek() == self.delimiter

  def tokenize(self, tokenizer):
    tokenizer.nxcharacter() # eat the hash character
    return tokenizer.build_token('comment','comment', lambda t : t.peek() != '\n' and not t.is_eof())