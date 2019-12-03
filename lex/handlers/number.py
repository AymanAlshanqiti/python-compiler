from lex.tokenizer import *
from lex.token import *

class NumberTokenHandler(TokenHandler):
  def __init__(self):
    self.digits = {
      'b': '01',
      'o': '01234567',
      'x': '0123456789abcdefABCDEF'
    }

    self.radix = {
      'b': 2,
      'o': 8,
      'x': 16
    }

  def is_tokenizable(self, tokenizer):
    return tokenizer.peek().isdigit()

  def tokenize(self, tokenizer):
    token = tokenizer.build_default_token('literal','number')
    if tokenizer.character() == '0':
      if tokenizer.peek() in 'box':
        token.value += tokenizer.nxcharacter()
        return self._tokenize_digit(tokenizer, token, tokenizer.character())

    token.add_metadata('datatype', 'integer')
    token.add_metadata('radix', 10)
    token.value += tokenizer.loop(lambda t: t.peek().isdigit())
    self._floatify(tokenizer, token)

    return token
  
  def _tokenize_digit(self, tokenizer, token, digit_prefix):
    token.value += tokenizer.loop(lambda t: t.peek() in self.digits[digit_prefix])

    if token.value != '0' + digit_prefix:
      token.category = 'literal'
      token.type = 'number'
      token.add_metadata('datatype', 'integer')
      token.add_metadata('radix', self.radix[digit_prefix])
      return token
    
    tokenizer.unexpected_token()
  
  def _floatify(self, tokenizer, token):
    # tokenizer floating point numbrer
    if tokenizer.peek() == '.':
      token.value += tokenizer.nxcharacter()
      if not tokenizer.is_peekable() or not tokenizer.peek().isdigit():
        tokenizer.unexpected_token()
      
      token.value += tokenizer.loop(lambda t: t.peek().isdigit())
      token.add_metadata('datatype', 'float')
  
# digits 0xhexa 0bbinary 0ooctal digits.digits