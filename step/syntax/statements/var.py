from step.lex.token import Token, EOFToken
from step.syntax.types import *
from step.syntax.handler import *
from step.symt.symboletable import *

# var datatype id [= expression]
class VarStatement(Statement):
  def __init__(self, symt_entry=None, token=None, datatype=None, identifier=None, expression=None, level=0, parent_stmt=None, next_stmt=None,previous_stmt=None):
    super().__init__(token, level, parent_stmt, next_stmt,previous_stmt)
    self.datatype = datatype
    self.identifier = identifier
    self.expression = expression
    self.symt_entry = None

class VarStatementParser(ParserHandler):
  def is_parsable(self, parser):
    token = parser.token
    return token.category == 'keyword' and token.value == 'var'

  def parse(self, parser, parent=None):
    token = parser.token
    
    parser.expect('keyword', 'keyword')
    if not parser.token.value in ['int', 'float', 'string', 'boolean']:
      parser.syntax_error()

    datatype = parser.token
    parser.expect('id', 'id')
    identifier = parser.token

    if parser.nxtoken.value == '=':
      parser.consume()
      expression = parser.expression()
    else:
      expression = None

    # symbol table entry
    symt_entry = SymtEntry(identifier.value,'var',{
      'value': expression.evalute().gattrs['value'],
      'datatype': datatype.value,
      'line_number': token.line_number
    })

    if parent != None:
      parent.symt.insert(symt_entry)
    else: # global symt
      parser.symt.insert(symt_entry)

    return VarStatement(symt_entry, token, datatype, identifier, expression, parser.statement_level, parent)