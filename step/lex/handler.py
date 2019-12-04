from abc import ABC, abstractclassmethod
from step.lex.token import *

class TokenHandler(ABC):
  def __init__(self):
    self.is_skipped = False

  @abstractclassmethod
  def is_tokenizable(self, tokenizer):
    return False

  @abstractclassmethod
  def tokenize(self, tokenizer):
    return None

