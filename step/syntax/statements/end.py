from step.lex.token import Token, EOFToken
from step.syntax.types import *
from step.syntax.handler import *

class EndStatementParser(ParserHandler):
  def is_parsable(self, parser):
    token = parser.token
    return token.category == 'keyword' and token.value == 'end'

  def parse(self, parser, parent=None):
    parser.exit_level_falg = True
    parser.current_level -= 1
    return None
