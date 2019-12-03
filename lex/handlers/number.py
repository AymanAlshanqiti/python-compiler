from lex.tokenizer import *
from lex.token import *

class NumberTokenHandler(TokenHandler):
  
  def is_tokenizable(self, tokenizer):
    return tokenizer.peek().isdigit()

  def tokenize(self, tokenizer):
    token = self.create_token(tokenizer, 'literal','number')
   
    #binary, octal, or hexadecimal
    if tokenizer.character() == '0':
      if tokenizer.peek() in 'box':
        token.value += tokenizer.nxcharacter()
        return self._tokenize_digit(tokenizer, token, tokenizer.character())

    #decimal
    token.add_metadata('datatype', 'integer')
    token.add_metadata('radix', 10)

    while tokenizer.is_peekable() and tokenizer.peek().isdigit():
      token.value += tokenizer.nxcharacter()

    # tokenizer floating point numbrer
    if tokenizer.peek() == '.':
      token.value += tokenizer.nxcharacter()
      if not tokenizer.is_peekable() or not tokenizer.peek().isdigit():
        tokenizer.unexpected_token()
      
      token.value += tokenizer.nxcharacter()

      while tokenizer.is_peekable() and tokenizer.peek().isdigit():
        token.value += tokenizer.nxcharacter()
      
      token.add_metadata('datatype', 'float')

    return token
  
  def _tokenize_digit(self, tokenizer, token, digit_prefix):
    digits = {
      'b': '01',
      'o': '01234567',
      'x': '0123456789abcdefABCDEF'
    }

    radix = {
      'b': 2,
      'o': 8,
      'x': 16
    }

    while tokenizer.is_peekable() and tokenizer.peek() in digits[digit_prefix]:
      token.value += tokenizer.nxcharacter()
    
    if token.value != '0' + digit_prefix:
      token.category = 'literal'
      token.type = 'number'
      token.add_metadata('datatype', 'integer')
      token.add_metadata('radix', radix[digit_prefix])
      return token
    
    tokenizer.unexpected_token()
  
# digits 0xhexa 0bbinary 0ooctal digits.digits