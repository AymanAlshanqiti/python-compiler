from token import Token

class Tokenizer:
  def __init__(self, source_code):
    self.line_number = 1
    self.position = 0
    self.source_code = source_code
    self.length = len(self.source_code)
    self.keywords = ['if', 'else', 'for', 'echo', 'break', 'while', 'switch']
    # self.tokens = []

  @property
  def is_eof(self):
    return self.position >= self.length 
  
  @property
  def character(self):
    return self.source_code[self.position]
  
  def read_variable(self):
    token = Token()
    token.token_line_number = self.line_number
    token.token_position = self.position
    token.token_type = 'variable'
    token.token_value = self.character
    self.position += 1
    while self.character.isalnum() or self.character == '_':
      token.token_value += self.character
      self.position += 1
    
    return token

  def read_space(self):
    token = Token()
    if self.character == '\n':
      self.line_number += 1
      token.token_type = 'new_line'
    else:
      token.token_type = 'space'
    token.token_line_number = self.line_number
    token.token_position = self.position
    token.token_value = self.character
    self.position += 1
    while self.character.isspace():
      token.token_value += self.character
      self.position += 1
    
    return token

  def read_number(self):
    token = Token()
    token.token_type = 'number'
    token.token_value = self.character
    self.position += 1
    token.token_line_number = self.line_number
    token.token_position = self.position
    while self.character.isdigit():
      token.token_value += self.character
      self.position += 1
    
    return token

  def read_assign_op(self):
    token = Token()
    token.token_type = 'assign'
    token.token_value = self.character
    self.position += 1
    token.token_line_number = self.line_number
    token.token_position = self.position

    return token

  def read_semicolon(self):
    token = Token()
    token.token_type = 'semicolon'
    token.token_value = self.character
    self.position += 1
    token.token_line_number = self.line_number
    token.token_position = self.position

    return token

  def read_keyword(self):
    token = Token()
    token.token_value = self.character
    self.position += 1
    while self.character.isalpha():
      token.token_value += self.character
      self.position += 1
    if token.token_value in self.keywords:
      token.token_type = 'keyword'

    return token

  def next_token(self):
    if self.character == '$':
      return self.read_variable()

    elif self.character.isspace():
      return self.read_space()

    elif self.character.isdigit():
      return self.read_number()
      
    elif self.character == '=':
      return self.read_assign_op()

    elif self.character == ';':
      return self.read_semicolon()

    elif self.character.isalpha():
      return self.read_keyword()

    else:
      print("error: Unexpected token")
      self.position += 1
    
  def __iter__(self):
    return self

  def __next__(self):
    if self.is_eof:
      raise StopIteration

    return self.next_token()
