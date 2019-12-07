from step.lex.tokenizer import *
from step.lex.handler import *
from step.src.sourcecode import SourceCode

class Tokenizer:
  def __init__(self, source_code, handlers=[], skipped_tokens = []):
    self.src = SourceCode(source_code)
    self.handlers = handlers
    self.tokens = []
    self.skipped_tokens = skipped_tokens

  def next_token(self):
    if not self.is_peekable():
      return EOFToken
    
    while self.is_peekable():
      for handler in self.handlers:
        if isinstance(handler, TokenHandler) and handler.is_tokenizable(self):
          token =  handler.tokenize(self)
          if not handler.is_skipped:
            return token
          else:
            break
  
    if not self.is_peekable():
      return EOFToken
  
    self.unexpected_token()
  
  def reset(self):
    self.line_number = 1
    self.position = -1

  def loop(self, expression):
    if not callable(expression):
      raise Exception("Invalid loop expression")
    token_value = ''
    while self.is_peekable() and expression(self):
      token_value += self.nxcharacter()
    return token_value

  def build_token(self, category=None, ttype=None, expression = False):
    token = Token(category, ttype, self.nxcharacter(), self.line_number, self.position)
    token.value += self.loop(expression)
    return token
  
  def build_default_token(self, category, ttype):
    return Token(category,ttype, self.nxcharacter(), self.line_number, self.position)

  def __iter__(self):
    return self

  def __next__(self):
    token = self.next_token()
    if token == EOFToken:
      raise StopIteration
    return token
  
  def unexpected_token(self):
    if not self.is_eof():
      print("Unexpected token '%s', line number : %d, position: %d" % (self.peek(), self.line_number, self.position))
    else:
      print("Unexpected token '%s', line number : %d, position: %d" % ('EOF', self.line_number, self.position))
    exit(0)
  

    
  

    
  