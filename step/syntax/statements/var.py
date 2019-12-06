from step.lex.token import Token, EOFToken
from step.syntax.types import *
from step.syntax.handler import *

# var | let datatype id [= expression]
class VarStatement(Statement):
  def __init__(self, token=None, datatype=None, identifier=None, expression=None, level=0, symt_entry=None, parent_stmt=None, next_stmt=None,previous_stmt=None):
    super().__init__(token, level, parent_stmt, next_stmt,previous_stmt)
    self.datatype = datatype
    self.identifier = identifier
    self.expression = expression
    self.symt_entry = symt_entry


class VarStatementParser(ParserHandler):
  def is_parsable(self, parser):
    token = parser.token
    return token.category == 'keyword' and token.value == 'var'

  def parse(self, parser, parent=None):
    statement = VarStatement(parser.token, None, None, None, parser.statement_level, None, parent)
    parser.expect('keyword', 'keyword')
    if not parser.token.value in ['int', 'float', 'string', 'boolean']:
      parser.syntax_error()

    statement.datatype = parser.token
    parser.expect('id', 'id')
    statement.identifier = parser.token

    if parser.nxtoken.value == '=':
      parser.consume()
      statement.expression = parser.expression()
    else:
      statement.expression = None
    
    statement.symt_entry = SymtEntry(statement.identifier.value, 'var',{
      'type': statement.datatype.value,
      'line_number': statement.token.line_number
    })

    parser.current_symt.insert(statement.symt_entry)

    return statement
