from lex.tokenizer import *
from lex.token import *

class NumberTokenHandler(TokenHandler):
  
  def is_tokenizable(self, tokenizer):
    return tokenizer.character.isdigit()

  def tokenize(self, tokenizer):
    token = self.token_init(tokenizer, 'number', 'integer')
    if tokenizer.character == '0':
      if tokenizer.peek == 'x':
        token.value += tokenizer.next_character
        return self.tokenize_hexadecimal(tokenizer, token)
      elif tokenizer.peek == 'o':
        token.value += tokenizer.next_character
        return self.tokenize_octal(tokenizer, token)
      elif tokenizer.peek == 'b':
        token.value += tokenizer.next_character
        return self.tokenize_binary(tokenizer, token)

    return token
  
  def tokenize_hexadecimal(self, tokenizer, token):
    while not tokenizer.is_eof and tokenizer.next_character in '1234567890abcdefABCDEF':
      token.value += tokenizer.character
    
    if token.value != '0x':
      token.category = 'literal'
      token.type = 'number'
      token.add_metadata('datatype', 'integer')
      token.add_metadata('radix', 16)
      return token
    
    tokenizer.unexpected_token()
  
  def tokenize_octal(self, tokenizer, token):
    while not tokenizer.is_eof and tokenizer.next_character in '01234567':
      token.value += tokenizer.character
    
    if token.value != '0o':
      token.category = 'literal'
      token.type = 'number'
      token.add_metadata('datatype', 'integer')
      token.add_metadata('radix', 8)
      return token
    
    tokenizer.unexpected_token()

  def tokenize_binary(self, tokenizer, token):
    while not tokenizer.is_eof and tokenizer.next_character in '01':
      token.value += tokenizer.character
    
    if token.value != '0b':
      token.category = 'literal'
      token.type = 'number'
      token.add_metadata('datatype', 'integer')
      token.add_metadata('radix', 2)
      return token
    
    tokenizer.unexpected_token()


# digits 0xhexa 0bbinary 0ooctal digits.digits