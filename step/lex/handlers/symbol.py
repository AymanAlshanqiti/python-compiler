from step.lex.handler import TokenHandler
from step.lex.token import Token

class SymbolTokenHandler(TokenHandler):
  def __init__(self, token_category=None, symboles={}):
    super().__init__()
    self.symbols = symboles
    self.token_category = token_category

  def is_tokenizable(self, tokenizer):
    return tokenizer.peek() in self.symbols.keys()

  def tokenize(self, tokenizer):
    ch = tokenizer.peek()
    target_record = self.symbols[ch]
    token = tokenizer.build_default_token(self.token_category, target_record[0][ch])
    
    for i in range(1, len(target_record)):
      ch = tokenizer.peek()
      if ch in target_record[i].keys():
        token.value += tokenizer.nxcharacter()
        token.type =  target_record[i][ch]
      else:
        break
    
    return token

