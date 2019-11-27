from token_handler import *
from token import EOFToken

class Tokenizer:
  def __init__(self, source_code, handlers=[]):
    self.line_number = 1
    self.position = 0
    self.source_code = source_code
    self.length = len(self.source_code)
    self.handlers = handlers

  @property
  def is_eof(self):
    return self.position >= self.length 
  
  @property
  def character(self):
    if not self.is_eof:
      return self.source_code[self.position]
    else:
      return None

  def next_token(self):
    
    if self.is_eof:
      return EOFToken
    
    wshandler =  WhitespaceTokenHandler()
    if(wshandler.is_readable(self)):
      wshandler.tokenize(self)
    
    if self.is_eof:
      return EOFToken

    for handler in self.handlers:
      if handler.is_readable(self):
        return handler.tokenize(self)
    
    self.unexpected_token()
  
  def reset(self):
    self.line_number = 1
    self.position = 0

  def read_all(self):
    self.reset()
    tokens = []
    for token in self:
      tokens.append(token)
    
    tokens.append(EOFToken)
    return tokens

  def unexpected_token(self):
    print("Unexpected token '%s'" % self.character)

  def __iter__(self):
    return self

  def __next__(self):
    token = None
    if self.is_eof :
      raise StopIteration

    token = self.next_token()
    if token is None:
      raise StopIteration

    return token
