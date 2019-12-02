from token import Token, EOFToken
from parser import *


class PrintStatement(Statement):
  def __init__(self, token=None, expression=None, level=0, parent_stmt=None, next_stmt=None,previous_stmt=None):
    super().__init__(token, level, parent_stmt, next_stmt,previous_stmt)
    self.expression = expression


class PrintStatementParser(ParserHandler):
  def is_parsable(self, parser):
    token = parser.tokenizer.token
    return token.category == 'keyword' and token.value == 'print'

  def parse(self, parser, parent=None):
    statement = PrintStatement(parser.tokenizer.token, parser.expression(), parser.current_level)
    statement.expression = parser.expression()
    return statement
