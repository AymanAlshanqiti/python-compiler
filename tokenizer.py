from token_handler import *


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
    return self.source_code[self.position]

  def next_token(self):

    for handler in self.handlers:
      if handler.is_readable(self):
        return handler.tokenize(self)
    
    self.unexpected_token()

  def unexpected_token(self):
    print("Unexpected token '%s'" % self.character)

  def __iter__(self):
    return self

  def __next__(self):
    if self.is_eof:
      raise StopIteration

    return self.next_token()
