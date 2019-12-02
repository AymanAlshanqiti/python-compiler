from abc import ABC, abstractclassmethod
from lex.token import *

class TokenHandler(ABC):
  def __init__(self):
    pass
  
  @abstractclassmethod
  def is_tokenizable(self, tokenizer):
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