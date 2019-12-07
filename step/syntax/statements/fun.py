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
    super().__init__('function', parent_symt,token, statements, level, parent_stmt, next_stmt, previous_stmt)
    self.parameters = params_list


class FunStatementParser(ParserHandler):
  def is_parsable(self, parser):
    token = parser.token
    return token.category == 'keyword' and token.value == 'fun'

  def parse(self, parser, parent=None):
    token = parser.token

    parser.expect('keyword', 'keyword')
    if not parser.token.value in ['int', 'float', 'string', 'boolean']:
      parser.syntax_error()

    datatype = parser.token
    parser.expect('id', 'id')
    identifier = parser.token

    statement = FunStatement(parser.symt, token, datatype, identifier, [], None, parser.statement_level, parent)
    
    parser.expect('punctuation', 'left_paren')
    statement.parameters = self.parse_params_list(statement.symt, parser)
    parser.expect('punctuation', 'right_paren')

    parser.statement_level += 1
    if parser.statement_level > 1:
      raise Exception('Invalid function definition')

    statement.statements = parser.parse(statement)

    # symbol table entry
    parser.symt.assert_duplication(identifier.value)

    symt_entry = SymtEntry(identifier.value,'function',{
      'return_type': datatype.value,
      'parameters' : {'count': len(statement.parameters)},
      'symt': statement.symt,
      'line_number': statement.token.line_number
    })

    parser.symt.insert(symt_entry)



    return statement
  
  def parse_params_list(self, symt, parser):
    params_list = []
    current_param_position = 0

    if parser.nxtoken.value == ')': # function without parameters
      return params_list
    
    params_list.append(self.parse_param(symt, parser, None, current_param_position))
    while parser.nxtoken.value == ',':
      parser.consume()
      current_param_position += 1
      params_list.append(self.parse_param(symt, parser, None, current_param_position))
    
    return params_list
  
  def parse_param(self, symt, parser, default_value = None, position=0):    
    parser.expect('keyword', 'keyword')
    if not parser.token.value in ['int', 'float', 'string', 'boolean']:
      parser.syntax_error()

    datatype = parser.token
    parser.expect('id', 'id')
    identifier = parser.token

    # symbol table entry
    symt.assert_duplication(identifier.value)

    symt_entry = SymtEntry(identifier.value,'parameter',{
      'value': 0,
      'datatype': datatype.value,
      'line_number': datatype.line_number
    })

    symt.insert(symt_entry)

    return FunParameter(datatype, identifier, default_value, position)
    
