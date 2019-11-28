from token import *
from tokenizer import *

class Node:
  def __init__(self, node_type):
    self.type = node_type
    self.line_number = 1
    self.position = 0
    self.level = 0

class BlockNode(Node):
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
    self.type = None
    self.value = value


# print value
class PrintNode(Node):
  def __init__(self, value=None):
    super().__init__('print')
    self.value = value

# var datatype id = value
class VarNode(Node):
  def __init__(self, datatype=None, identifier=None, value=None):
    super().__init__('variable')
    self.datatype = datatype
    self.identifier = identifier
    self.value = value

# for init_number to last_number statements end
class ForNode(BlockNode):
  def __init__(self, init_number=None, last_number=None, statements=[]):
    super().__init__('for', statements)
    self.init_number = init_number
    self.last_number = last_number

# fun datatype id() statements end
class FunNode(BlockNode):
  def __init__(self, datatype=None, identifire=None, statements=[]):
    super().__init__('fun', statements)
    self.datatype = datatype
    self.identifier = identifire


# while value statements end

class WhileNode(BlockNode):
  def __init__(self, value=None, statements=[]):
    super().__init__('while', statements)
    self.value = value

class Parser:
  def __init__(self, tokenizer):
    self.token = None
    self.current_level = 0
    self.current_level_name = ''
    self.tokenizer = tokenizer

  def syntax_error(self, message, line_number, position):
    print('Ay syntax error:' + message + ', line number : ' + str(line_number) + ', position: ' + str(position))
    exit(0)

  def end_statement(self):
    if self.token.category != 'keyword' or self.token.value != 'end':
      self.syntax_error('"end" keyword expected', self.token.line_number, self.token.position)
  
  def parse_print(self):
    print_statement = PrintNode()
    print_statement.line_number = self.token.line_number
    print_statement.position = self.token.position
    print_statement.level = self.current_level

    # 1. Check value token 
    self.token = self.tokenizer.next()
    #self.tokenizer.next_token()
    if self.token.category == 'keyword':
      if self.token.type == 'literal':
        print_statement.value = self.token
        return print_statement
    elif self.token.category == 'number':
      print_statement.value = self.token
      return print_statement
    
    self.syntax_error("value expected", self.token.line_number, self.token.position)
    

  def parse_var(self):
    var_statement = VarNode()
    var_statement.line_number = self.token.line_number
    var_statement.position = self.token.position
    var_statement.level = self.current_level
    # var datatype id = value
    self.token = self.tokenizer.next()

    # 1. Check for datatype
    if self.token.category != 'keword' and self.token.type != 'datatype':
      self.syntax_error('datatype expected', self.token.line_number, self.token.position)
    
    var_statement.datatype = self.token

    # 2. Check for id
    self.token = self.tokenizer.next()
    if self.token.category != 'id':
      self.syntax_error('id expected', self.token.line_number, self.token.position)
    
    var_statement.identifier = self.token

    # 3. Check for =
    self.token = self.tokenizer.next()
    if self.token.category != 'punctuation' or self.token.type != 'assignment':
      self.syntax_error('assignment expected', self.token.line_number, self.token.position)
    
    # 4. Check for value
    self.token = self.tokenizer.next()
    if self.token.category == 'keyword' or self.token.category == 'number':
      if self.token.category == 'keyword':
        if self.token.type != 'literal':
          self.syntax_error('literal value expected', self.token.line_number, self.token.position)
      else: # number
        pass
    else:
      self.syntax_error('literal keword or number expected', self.token.line_number, self.token.position)
    
    var_statement.value = self.token
    return var_statement
  
  def match(self, token_category, token_type):
    self.token = self.tokenizer.next()
    if self.token.category != token_category or self.token.type != token_type:
      self.syntax_error('unexpected token', self.token.line_number, self.token.position)
   

  def parse_fun(self):
    if self.current_level != 0:
      self.syntax_error('invalid use of function', self.token.line_number, self.token.position)
    fun_statement = FunNode()
    fun_statement.line_number = self.token.line_number
    fun_statement.position = self.token.position
    fun_statement.level = self.current_level
    
    self.match('keyword','datatype')
    fun_statement.datatype = self.token
    self.match('id','id')
    fun_statement.identifier = self.token
    self.match('punctuation', 'parenl')
    self.match('punctuation', 'parenr')
 
    # 5. Read statements
    self.current_level += 1
    fun_statement.statements = self.parse()
    self.end_statement()

    return fun_statement
  
  def parse_for(self):
    for_statement = ForNode()
    for_statement.line_number = self.token.line_number
    for_statement.position  = self.token.position
    for_statement.level = self.current_level

    # 1. Check initial number
    self.token = self.tokenizer.next()
    if self.token.category != 'number':
      self.syntax_error("initial value must be a number", self.token.line_number, self.token.position)
    
    for_statement.init_number = self.token

    # 2. Check 'to' keyword
    self.token = self.tokenizer.next()

    if self.token.category != 'keyword' or self.token.value != 'to':
      self.syntax_error('"to" keyword expected', self.token.line_number, self.token.position)
    
    #3. Check last number
    self.token = self.tokenizer.next()
    if self.token.category != 'number':
      self.syntax_error("last value must be a number", self.token.line_number, self.token.position)
    
    for_statement.last_number = self.token

    #4. Read statements
    self.current_level += 1
    for_statement.statements = self.parse()

    if self.token.category != 'keyword' or self.token.value != 'end':
      self.syntax_error('"end" keyword expected', self.token.line_number, self.token.position)
    
    return for_statement
  
  def parse_while(self):
    while_statement = WhileNode()
    while_statement.line_number = self.token.line_number
    while_statement.position  = self.token.position
    while_statement.level = self.current_level

    # 1. Check value
    self.token = self.tokenizer.next()
    if self.token.category != 'number':
      self.syntax_error("value expected", self.token.line_number, self.token.position)
    
    while_statement.value = self.token

    #2. Read statements
    self.current_level += 1
    while_statement.statements = self.parse()

    if self.token.category != 'keyword' or self.token.value != 'end':
      self.syntax_error('"end" keyword expected', self.token.line_number, self.token.position)
    
    return while_statement
    
  #start expression apis
  
  def expression(self):
    expr = self.multiplication()
    operator = self.tokenizer.peek()
    while operator.value == '+' or operator.value == '-':
      self.tokenizer.next()
      right_expression = self.multiplication()
      expr = BinaryExpression(expr, operator, right_expression)
    
    return expr
  
  def multiplication(self):
    expr = self.primary()
    operator = self.tokenizer.peek()
    while operator.value == '/' or operator.value == '*':
      self.tokenizer.next()
      right_expression = self.primary()
      expr = BinaryExpression(expr, operator, right_expression)
    return expr
  
  def primary(self):
    self.token = self.tokenizer.peek()
    if self.token.category == 'number':
      return LiteralExpression('integer', token.value)
    elif self.token.category == 'keyword' and self.token.type == 'literal':
      if self.token.value == 'null':
        return LiteralExpression('null', token.value)
      else:
        return LiteralExpression('boolean', token.value)
    
    self.syntax_error('invalid literal value', self.token.line_number, self.token.position)
  


  #end expression apis
  def parse(self):
    statements = []
    self.token = self.tokenizer.next()
    if self.token.category == 'keyword' and self.token.value == 'end':
      self.current_level -= 1
      if self.current_level < 0:
        self.syntax_error('unexpected end', self.token.line_number, self.token.position)
      return statements # empty statement

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
        elif self.token.value == 'fun':
          self.current_level_name = self.token.value
          statements.append(self.parse_fun())
      
      self.token = self.tokenizer.next()
      if self.token.category == 'keyword' and self.token.value == 'end':
        self.current_level -= 1
        if self.current_level < 0:
          self.syntax_error('unexpected end', self.token.line_number, self.token.position)
        break

    return statements
