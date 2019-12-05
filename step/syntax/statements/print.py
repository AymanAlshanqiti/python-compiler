from step.lex.token import Token, EOFToken
from step.syntax.types import *
from step.syntax.handler import *

class PrintStatement(Statement):
  def __init__(self, token=None, expression=None, level=0, parent_stmt=None, next_stmt=None,previous_stmt=None):
    super().__init__(token, level, parent_stmt, next_stmt,previous_stmt)
    self.expression = expression


class PrintStatementParser(ParserHandler):
  def is_parsable(self, parser):
    token = parser.token
    return token.category == 'keyword' and token.value == 'print'

  def parse(self, parser, parent=None):
    statement = PrintStatement(parser.token, parser.expression(), parser.statement_level, parent)
    return statement
