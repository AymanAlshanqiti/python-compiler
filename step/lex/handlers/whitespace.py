from step.lex.handler import TokenHandler
from step.lex.token import Token

class WhitespaceTokenHandler(TokenHandler):

  def is_tokenizable(self, tokenizer):
    return tokenizer.peek().isspace()

  def tokenize(self, tokenizer):
    return tokenizer.build_token('space','space', lambda t : t.peek().isspace())