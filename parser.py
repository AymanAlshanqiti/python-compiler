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


# while value statements end

class WhileNode(BlockNode):
  def __init__(self, value=None, statements=[]):
    super().__init__('while', statements)
    self.value = value

class Parser:
  def __init__(self):
    self.token = None
    self.current_level = 0
    pass

  def syntax_error(self, message, line_number, position):
    print('Ay syntax error:' + message + ', line number : ' + str(line_number) + ', position: ' + str(position))
    exit(0)

  def parse_print(self, tokenizer):
    print_statement = PrintNode()
    print_statement.line_number = self.token.line_number
    print_statement.position = self.token.position
    print_statement.level = self.current_level

    # 1. Check value token 
    self.token = tokenizer.next_token()
    if self.token.category == 'keyword':
      if self.token.type == 'literal':
        print_statement.value = self.token
        return print_statement
    elif self.token.category == 'number':
      print_statement.value = self.token
      return print_statement
    
    self.syntax_error("value expected", self.token.line_number, self.token.position)
    

  def parse_var(self, tokenizer):
    var_statement = VarNode()
    var_statement.line_number = self.token.line_number
    var_statement.position = self.token.position
    var_statement.level = self.current_level
    # var datatype id = value
    self.token = tokenizer.next_token()

    # 1. Check for datatype
    if self.token.category != 'keword' and self.token.type != 'datatype':
      self.syntax_error('datatype expected', self.token.line_number, self.token.position)
    
    var_statement.datatype = self.token

    # 2. Check for id
    self.token = tokenizer.next_token()
    if self.token.category != 'id':
      self.syntax_error('id expected', self.token.line_number, self.token.position)
    
    var_statement.identifier = self.token

    # 3. Check for =
    self.token = tokenizer.next_token()
    if self.token.category != 'punctuation' or self.token.type != 'assignment':
      self.syntax_error('assignment expected', self.token.line_number, self.token.position)
    
    # 4. Check for value
    self.token = tokenizer.next_token()
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
  
  def parse_for(self, tokenizer):
    for_statement = ForNode()
    for_statement.line_number = self.token.line_number
    for_statement.position  = self.token.position
    for_statement.level = self.current_level

    # 1. Check initial number
    self.token = tokenizer.next_token()
    if self.token.category != 'number':
      self.syntax_error("initial value must be a number", self.token.line_number, self.token.position)
    
    for_statement.init_number = self.token

    # 2. Check 'to' keyword
    self.token = tokenizer.next_token()

    if self.token.category != 'keyword' or self.token.value != 'to':
      self.syntax_error('"to" keyword expected', self.token.line_number, self.token.position)
    
    #3. Check last number
    self.token = tokenizer.next_token()
    if self.token.category != 'number':
      self.syntax_error("last value must be a number", self.token.line_number, self.token.position)
    
    for_statement.last_number = self.token

    #4. Read statements
    self.current_level += 1
    for_statement.statements = self.parse(tokenizer)

    if self.token.category != 'keyword' or self.token.value != 'end':
      self.syntax_error('"end" keyword expected', self.token.line_number, self.token.position)
    
    return for_statement
  
  def parse_while(self, tokenizer):
    while_statement = WhileNode()
    while_statement.line_number = self.token.line_number
    while_statement.position  = self.token.position
    while_statement.level = self.current_level

    # 1. Check value
    self.token = tokenizer.next_token()
    if self.token.category != 'number':
      self.syntax_error("value expected", self.token.line_number, self.token.position)
    
    while_statement.value = self.token

    #2. Read statements
    self.current_level += 1
    while_statement.statements = self.parse(tokenizer)

    if self.token.category != 'keyword' or self.token.value != 'end':
      self.syntax_error('"end" keyword expected', self.token.line_number, self.token.position)
    
    return while_statement
    
  
  def parse(self, tokenizer):
    statements = []
    self.token = tokenizer.next_token()
    if self.token.category == 'keyword' and self.token.value == 'end':
      self.current_level -= 1
      if self.current_level < 0:
        self.syntax_error('unexpected end', self.token.line_number, self.token.position)
      return statements # empty statement

    while self.token != EOFToken:
      if self.token.category == 'keyword':
        if self.token.value == 'var':
          statements.append(self.parse_var(tokenizer))
        elif self.token.value == 'print':
          statements.append(self.parse_print(tokenizer))
        elif self.token.value == 'for':
          statements.append(self.parse_for(tokenizer))
        elif self.token.value == 'while':
          statements.append(self.parse_while(tokenizer))
      
      self.token = tokenizer.next_token()
      if self.token.category == 'keyword' and self.token.value == 'end':
        self.current_level -= 1
        if self.current_level < 0:
          self.syntax_error('unexpected end', self.token.line_number, self.token.position)
     
        break

    
    return statements
