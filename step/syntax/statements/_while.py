from step.lex.token import Token, EOFToken
from step.syntax.types import *
from step.syntax.handler import *

# while expression statements end

class BlockStatement(Statement):
  def __init__(self, token=None, level=0, parent_stmt=None, next_stmt=None,previous_stmt=None, statements=[]):
    super().__init__(token, level, parent_stmt, next_stmt,previous_stmt)
    self.statements = statements

class WhileStatement(BlockStatement):
  def __init__(self, token=None, expression=None, statements=[], level=0, parent_stmt=None, next_stmt=None,previous_stmt=None):
    super().__init__(self, token, level, parent_stmt, next_stmt,previous_stmt, statements)
    self.expression = expression


class WhileStatementParser(ParserHandler):
  def is_parsable(self, parser):
    token = parser.token
    return token.category == 'keyword' and token.value == 'while'

  def parse(self, parser, parent=None):
    statement = WhileStatement(parser.token, parser.expression(), [], parser.current_level, parent)
    parser.current_level += 1
    statement.statements = parser.parse(statement)
    return statement