from lex.tokenizer import *
from lex.handler import *

class WhitespaceTokenHandler(TokenHandler):

  def is_tokenizable(self, tokenizer):
    return tokenizer.character.isspace()

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'space','space')
    
    if tokenizer.character == '\n':
      tokenizer.line_number += 1

    tokenizer.position += 1
    while not tokenizer.is_eof and tokenizer.character.isspace():
      token.value += tokenizer.character
      tokenizer.position += 1
    return token

class Tokenizer:
  def __init__(self, source_code, handlers=[]):
    self.line_number = 1
    self.position = 0
    self.source_code = source_code
    self.length = len(self.source_code)
    self.handlers = handlers
    self.tokens = []

  @property
  def is_eof(self):
    return self.position >= self.length 
  
  @property
  def character(self):
    if not self.is_eof:
      return self.source_code[self.position]
    else:
      return None
  
  @property
  def next_character(self):
    try:
      self.position += 1
      return self.source_code[self.position]
    except:
      return '\0'
  
  @property
  def peek(self):
    try:
      return self.source_code[self.position + 1]
    except:
      return None

  def next_token(self):
    
    if self.is_eof:
      return EOFToken
    
    wshandler =  WhitespaceTokenHandler()
    if(wshandler.is_tokenizable(self)):
      wshandler.tokenize(self)
    
    if self.is_eof:
      return EOFToken

    for handler in self.handlers:
      if handler.is_tokenizable(self):
        return handler.tokenize(self)
    
    self.unexpected_token()
  
  def reset(self):
    self.line_number = 1
    self.position = 0

  def read_all(self):
    self.reset()
    self.tokens = []
    for token in self:
      self.tokens.append(token)
    
    self.tokens.append(EOFToken)
    return self.tokens

  def unexpected_token(self):
    if not self.is_eof:
      print("Unexpected token '%s', line number : %d, position: %d" % (self.character, self.line_number, self.position))
    else:
      print("Unexpected token '%s', line number : %d, position: %d" % ('EOF', self.line_number, self.position))


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


class TokenizerList:
  def __init__(self, source_code, handlers= []):
    self.tokens = Tokenizer(source_code, handlers).read_all()
    self.current = -1
  
  def has_token(self):
    return (self.current + 1) < len(self.tokens)

  def reset(self):
    self.current = -1
  
  @property
  def token(self):
    if not self.has_token():
      return EOFToken
    
    if self.current == -1:
      return ERRToken

    return self.tokens[self.current]
  
  def peek(self):
    if self.has_token():
      return self.tokens[self.current + 1]
    return EOFToken
  
  def next(self):
    if self.has_token():
      self.current += 1
      return self.token
    return EOFToken
  

    
  

    
  