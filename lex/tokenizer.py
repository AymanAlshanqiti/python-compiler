from lex.tokenizer import *
from lex.handler import *

NullCharacter = '\0'

class Tokenizer:
  def __init__(self, source_code, handlers=[]):
    self.line_number = 1
    self.position = -1
    self.source_code = source_code
    self.length = len(self.source_code)
    self.handlers = handlers
    self.tokens = []
  
  def is_eof(self):
    return self.position >= self.length 
  
  def is_peekable(self):
    return (self.position + 1) < self.length
  
  def character(self):
    if not self.is_eof() and self.position > -1:
      return self.source_code[self.position]
    else:
      return NullCharacter
  
  def peek(self):
    if self.is_peekable():
      return self.source_code[self.position + 1]
    return NullCharacter
  
  def nxcharacter(self):
    if self.is_peekable():
      self.position += 1
      if self.character() == '\n':
        self.line_number += 1
      return self.source_code[self.position]
    return NullCharacter

  def next_token(self):
    if not self.is_peekable():
      return EOFToken

    for handler in self.handlers:
      if handler.is_tokenizable(self):
        return handler.tokenize(self)
    
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
  

    
  

    
  