from step.lex.handler import TokenHandler
from step.lex.token import Token


class StringTokenHandler(TokenHandler):
  def is_tokenizable(self, tokenizer):
    return tokenizer.peek() == '"'

  def tokenize(self, tokenizer):
    tokenizer.nxcharacter()
    tmp_position = tokenizer.position
    if tokenizer.peek() == '"':
      tokenizer.nxcharacter()
      token =  Token('literal','string','', tokenizer.line_number, tmp_position)
      return token
    
    token =  tokenizer.build_default_token('literal', 'string')
    token.value += tokenizer.loop(lambda t: t.peek() != '"' and t.peek() != '\n')
    
    if tokenizer.peek() != '"':
      self.unexpcted_token()
    
    tokenizer.nxcharacter() # skip "
    return token