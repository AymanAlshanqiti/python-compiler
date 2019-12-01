from token import *
from tokenizer import *

class Statement:
  def __init__(self, node_type):
    self.type = node_type
    self.line_number = 1
    self.position = 0
    self.level = 0

class BlockStatement(Statement):
  def __init__(self, node_type, statements=[]):
    super().__init__(node_type)
    self.statements = statements

class Expression:
  def __init__(self):
    pass

class BinaryExpression(Expression):
  def __init__(self, left, operator, right):
    super().__init__()
    self.left_expression = left
    self.operator = operator
    self.right_expression = right

  
class UnaryExpression(Expression):
  def __init__(self, expression, operator):
    super().__init__()
    self.expression = expression
    self.operator = operator


class LiteralExpression(Expression):
  def __init__(self, type, value=None):
    super().__init__()
    self.type = type
    self.value = value

class IdentifierExpression(Expression):
  def __init__(self, identifier, value=None):
    super().__init__()
    self.identifier = identifier
    self.value = value


# print value
class PrintStatement(Statement):
  def __init__(self, expression=None):
    super().__init__('print')
    self.expression = expression

# var datatype id = value
class VarStatement(Statement):
  def __init__(self, datatype=None, identifier=None, expression=None):
    super().__init__('variable')
    self.datatype = datatype
    self.identifier = identifier
    self.expression = expression

# for init_number to last_number statements end
class ForStatement(BlockStatement):
  def __init__(self, from_expression=None, to_expression=None, statements=[]):
    super().__init__('for', statements)
    self.from_expression = from_expression
    self.to_expression = to_expression

# fun datatype id() statements end
class FunStatement(BlockStatement):
  def __init__(self, datatype=None, identifire=None, statements=[]):
    super().__init__('fun', statements)
    self.datatype = datatype
    self.identifier = identifire


# while value statements end

class WhileStatement(BlockStatement):
  def __init__(self, expression=None, statements=[]):
    super().__init__('while', statements)
    self.expression = expression

class Parser:
  def __init__(self, tokenizer):
    self.token = None
    self.current_level = 0
    self.current_level_name = ''
    self.tokenizer = tokenizer

  def syntax_error(self, message, line_number, position):
    print('Ay syntax error:' + message + ', line number : ' + str(line_number) + ', position: ' + str(position))
    exit(0)

  def init_statement(self, statement_object):
    statement = statement_object
    statement.line_number = self.token.line_number
    statement.position = self.token.position
    statement.level = self.current_level
    return statement
  
  def match(self, token_category, token_type):
    self.token = self.tokenizer.next()
    if self.token.category != token_category or self.token.type != token_type:
      self.syntax_error('unexpected token', self.token.line_number, self.token.position)
 
  def parse_print(self):
    print_statement = self.init_statement(PrintStatement())
    print_statement.expression = self.expression()
    return print_statement

  def parse_var(self):
    var_statement = self.init_statement(VarStatement())
    self.match('keyword', 'datatype')
    var_statement.datatype = self.token
    self.match('id', 'id')
    var_statement.identifier = self.token
    self.match('punctuation', 'assignment')
    var_statement.expression = self.expression()
  
    return var_statement  
  
  def parse_for(self):
    for_statement = self.init_statement(ForStatement())
    for_statement.from_expression = self.expression()
    self.match('keyword','to') 
    for_statement.to_expression = self.expression()

    self.current_level += 1
    for_statement.statements = self.parse()
    
    return for_statement
  
  def parse_while(self):
    while_statement = self.init_statement(WhileStatement())
    while_statement.expression = self.expression()

    self.current_level += 1
    while_statement.statements = self.parse()

    return while_statement
    
  #start expression apis
  
  def expression(self):
    expr = self.multiplication()
    operator = self.tokenizer.peek()
    while operator.value == '+' or operator.value == '-':
      self.tokenizer.next()
      right_expression = self.multiplication()
      expr = BinaryExpression(expr, operator, right_expression)
      operator = self.tokenizer.peek()
    
    return expr


  def multiplication(self):
    expr = self.primary()
    operator = self.tokenizer.peek()
    while operator.value == '/' or operator.value == '*':
      self.tokenizer.next()
      right_expression = self.primary()
      expr = BinaryExpression(expr, operator, right_expression)
      operator = self.tokenizer.peek()
    return expr
  
  def primary(self):
    self.token = self.tokenizer.peek()
    if self.token == EOFToken:
      return None

    expr = None
    if self.token.category == 'number':
      expr = LiteralExpression('integer', self.token.value)
      self.token = self.tokenizer.next()
      return expr
    elif self.token.category == 'id':
      expr = IdentifierExpression('identifier', self.token.value)
      self.token = self.tokenizer.next()
      return expr
    elif self.token.category == 'keyword' and self.token.type == 'literal':
      if self.token.value == 'null':
        expr = LiteralExpression('null', self.token.value)
        self.token = self.tokenizer.next()
        return expr
      else:
        expr = LiteralExpression('boolean', self.token.value)
        self.token = self.tokenizer.next()
        return expr
    elif self.token.category == 'punctuation' and self.token.type == 'parenl':
      self.tokenizer.next()
      expr = self.expression()
      self.match('punctuation', 'parenr')
      return expr

    self.syntax_error('invalid value ' + self.token.value, self.token.line_number, self.token.position)
  
  #end expression apis
  def parse(self):
    statements = []
    self.token = self.tokenizer.next()

    while self.token != EOFToken:
      if self.token.category == 'keyword':
        if self.token.value == 'var':
          statements.append(self.parse_var())
        elif self.token.value == 'print':
          statements.append(self.parse_print())
        elif self.token.value == 'for':
          self.current_level_name = self.token.value
          statements.append(self.parse_for())
        elif self.token.value == 'while':
          self.current_level_name = self.token.value
          statements.append(self.parse_while())
        elif self.token.value == 'end':
          self.current_level -= 1
          if self.current_level < 0:
            self.syntax_error('unexpected end', self.token.line_number, self.token.position)
          return statements # empty statement
      
      self.token = self.tokenizer.next()

    return statements

  def has_error(self):
    return not self.current_level == 0
