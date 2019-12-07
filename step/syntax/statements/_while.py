from step.lex.token import Token, EOFToken
from step.syntax.types import *
from step.syntax.handler import *
from step.symt.symboletable import *

# while expression statements end

class WhileStatement(BlockStatement):
  def __init__(self, parent_symt, token=None, expression=None, statements=[], level=0, parent_stmt=None, next_stmt=None,previous_stmt=None):
    super().__init__('while', parent_symt,token, statements, level, parent_stmt, next_stmt, previous_stmt)
    self.expression = expression


class WhileStatementParser(ParserHandler):
  def is_parsable(self, parser):
    token = parser.token
    return token.category == 'keyword' and token.value == 'while'

  def parse(self, parser, parent=None):
    
    if parent != None:
      psymt = parent.symt
    else:
      psymt = parser.symt

    statement = WhileStatement(psymt, parser.token, parser.expression(), [], parser.statement_level, parent)
    parser.statement_level += 1
    statement.statements = parser.parse(statement)

    return statement
