from step.lex.token import Token, EOFToken
from step.syntax.types import *
from step.syntax.handler import *

# while expression statements end
# def __init__(self, token=None, level=0, parent_stmt=None, next_stmt=None,previous_stmt=None, statements=[]):
class WhileStatement(BlockStatement):
  def __init__(self, token=None, expression=None, statements=[], level=0, parent_stmt=None, next_stmt=None,previous_stmt=None, parent_symt=None):
    super().__init__(token, level, parent_stmt, next_stmt,previous_stmt, statements, parent_symt)
    self.expression = expression


class WhileStatementParser(ParserHandler):
  def is_parsable(self, parser):
    token = parser.token
    return token.category == 'keyword' and token.value == 'while'

  def parse(self, parser, parent=None):
    statement = WhileStatement(parser.token, parser.expression(), [], parser.statement_level, parent, None, None, parser.current_symt)
    parser.statement_level += 1
    statement.statements = parser.parse(statement)
    return statement
