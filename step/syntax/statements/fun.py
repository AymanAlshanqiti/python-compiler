from step.lex.token import Token, EOFToken
from step.syntax.types import *
from step.syntax.handler import *
from step.symt.symboletable import *

# fun datatype id (parms_list) statements end
# parms_list -> [param [, param]]
# param -> datatype id

class FunParameter:
  def __init__(self, datatype=None, identifier=None,default_value=None, position = 0):
    self.datatype = datatype
    self.identifier = identifier
    self.default_value = default_value
    self.position = position

class FunStatement(BlockStatement):
  def __init__(self, parent_symt, token=None, datatype=None, identifier=None, params_list = [], statements=[], level=0, parent_stmt=None, next_stmt=None,previous_stmt=None):
    super().__init__(parent_symt,token, statements, level, parent_stmt, next_stmt, previous_stmt)
    self.expression = expression
    self.parameters = params_list


class FunStatementParser(ParserHandler):
  def is_parsable(self, parser):
    token = parser.token
    return token.category == 'keyword' and token.value == 'fun'

  def parse(self, parser, parent=None):
    token = parser.token

    if parent != None:
      psymt = parent.symt
    else:
      psymt = parser.symt
    
    parser.expect('keyword', 'keyword')
    if not parser.token.value in ['int', 'float', 'string', 'boolean']:
      parser.syntax_error()

    datatype = parser.token
    parser.expect('id', 'id')
    identifier = parser.token

    parser.expect('punctuation', 'left_paren')
    parameters = self.parse_params_list(parser)
    parser.expect('punctuation', 'right_paren')

    statement = FunStatement(psymt, token, datatype, identifier, parameters, None, parser.statement_level, parent)
    parser.statement_level += 1
    statement.statements = parser.parse(statement)

    return statement
  
  def parse_params_list(self, parser):
    params_list = []
    current_param_position = 0

    if parser.nxtoken.value == ')': # function without parameters
      return params_list
    
    params_list.append(self.parse_param(parser, None, current_param_position))
    while parser.nxtoken.value == ',':
      parser.consume()
      current_param_position += 1
      params_list.append(self.parse_param(parser, None, current_param_position))
    
    return params_list
  
  def parse_param(self, parser, default_value = None, position=0):    
    parser.expect('keyword', 'keyword')
    if not parser.token.value in ['int', 'float', 'string', 'boolean']:
      print('xxxx')
      parser.syntax_error()

    datatype = parser.token
    parser.expect('id', 'id')
    identifier = parser.token
    return FunParameter(datatype, identifier, default_value, position)
    
