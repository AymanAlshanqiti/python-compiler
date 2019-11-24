from abc import ABC, abstractclassmethod
from token import Token

class TokenHandler(ABC):
  def __init__(self):
    pass
  
  @abstractclassmethod
  def is_readable(self, tokenizer):
    return False

  @abstractclassmethod
  def tokenize(self, tokenizer):
    return None

  def token_init(self, tokenizer, token_type):
    token = Token()
    token.line_number = tokenizer.line_number
    token.position = tokenizer.position
    token.type = token_type
    token.value = tokenizer.character

    return token


class VariableTokenHandler(TokenHandler):

  def is_readable(self, tokenizer):
    return tokenizer.character == '$'

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'variable')
    tokenizer.position += 1
    while tokenizer.character.isalnum() or tokenizer.character == '_':
      token.value += tokenizer.character
      tokenizer.position += 1
    return token


class WhitespaceTokenHandler(TokenHandler):

  def is_readable(self, tokenizer):
    return tokenizer.character.isspace()

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'space')
    
    if tokenizer.character == '\n':
      tokenizer.line_number += 1

    tokenizer.position += 1
    while tokenizer.character.isspace():
      token.value += tokenizer.character
      tokenizer.position += 1
    return token


class NumberTokenHandler(TokenHandler):

  def is_readable(self, tokenizer):
    return tokenizer.character.isdigit()

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'number')
    tokenizer.position += 1

    while tokenizer.character.isdigit():
      token.value += tokenizer.character
      tokenizer.position += 1
    return token


class OneCharacterTokenHandler(TokenHandler):
  def __init__(self):
    self.characters = {
      ';': 'simicolon', 
      '=': 'assign', 
      '{': 'curlyl', 
      '}': 'curlyr', 
      '(': 'parenl', 
      ')': 'parenr',
      ',': 'comma'
    }

  def is_readable(self, tokenizer):
    return tokenizer.character in self.characters.keys()

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, self.characters[tokenizer.character])
    tokenizer.position += 1
    return token



class IdTokenHandler(TokenHandler):
  def __init__(self):
    self.keywords = ['if', 'else', 'for', 'echo', 'break', 'while', 'switch', 'print',
    'function', 'return']

  def is_readable(self, tokenizer):
    return tokenizer.character.isalpha() or tokenizer.character == '_'

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'id')
    tokenizer.position += 1

    while tokenizer.character.isalnum() or tokenizer.character == '_':
      token.value += tokenizer.character
      tokenizer.position += 1

    if token.value in self.keywords:
      token.type = 'keyword' 
    return token



class CommentTokenHandler(TokenHandler):

  def is_readable(self, tokenizer):
    return tokenizer.character == '#'

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'comment')
    tokenizer.position += 1
    while not tokenizer.character == '\n':
      token.value += tokenizer.character
      tokenizer.position += 1
    return token
