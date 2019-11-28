from abc import ABC, abstractclassmethod
from token import Token, EOFToken

class TokenHandler(ABC):
  def __init__(self):
    pass
  
  @abstractclassmethod
  def is_readable(self, tokenizer):
    return False

  @abstractclassmethod
  def tokenize(self, tokenizer):
    return None

  def token_init(self, tokenizer, token_category, token_type):
    token = Token()
    token.line_number = tokenizer.line_number
    token.position = tokenizer.position
    token.category = token_category
    token.type = token_type
    token.value = tokenizer.character

    return token

class WhitespaceTokenHandler(TokenHandler):

  def is_readable(self, tokenizer):
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


class NumberTokenHandler(TokenHandler):

  def is_readable(self, tokenizer):
    return tokenizer.character.isdigit()

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'number', 'integer')
    tokenizer.position += 1

    while not tokenizer.is_eof and tokenizer.character.isdigit():
      token.value += tokenizer.character
      tokenizer.position += 1
    return token


class OneCharacterTokenHandler(TokenHandler):
  def __init__(self):
    self.characters = {
      ';': 'simicolon', 
      '=': 'assignment', 
      '{': 'curlyl', 
      '}': 'curlyr', 
      '(': 'parenl', 
      ')': 'parenr',
      ',': 'comma',
      '+': 'plus',
      '-': 'minus',
      '/': 'division',
      '*': 'multiplication'
    }

  def is_readable(self, tokenizer):
    return tokenizer.character in self.characters.keys()

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'punctuation', self.characters[tokenizer.character])
    tokenizer.position += 1
    return token


class IdTokenHandler(TokenHandler):
  def __init__(self):
    self.keywords = ['var','fun', 'if', 'else', 'for','end','to', 'echo', 'break', 'while', 'switch', 'print',
    'function', 'return', 'integer', 'float', 'char', 'boolean', 'true', 'false', 'null']
    self.datatypes = ['integer', 'float', 'char', 'boolean']
    self.literals = ['true', 'false', 'null']

  def is_readable(self, tokenizer):
    return tokenizer.character.isalpha() or tokenizer.character == '_'

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'id', 'id')
    tokenizer.position += 1
    while not tokenizer.is_eof and (tokenizer.character.isalnum() or tokenizer.character == '_'):
      token.value += tokenizer.character
      tokenizer.position += 1

    if token.value in self.keywords:
      token.category = 'keyword'

      if token.value in self.datatypes:
        token.type = 'datatype'
      elif token.value in self.literals:
        token.type = 'literal'
      else:
        token.type = token.value

           
    return token



class CommentTokenHandler(TokenHandler):

  def is_readable(self, tokenizer):
    return tokenizer.character == '#'

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'comment','comment')
    tokenizer.position += 1
    while not tokenizer.is_eof and not tokenizer.character == '\n':
      token.value += tokenizer.character
      tokenizer.position += 1
    return token
