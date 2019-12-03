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

