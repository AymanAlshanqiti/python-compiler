from step.lex.token import *
from step.lex.tokenizer import *
from step.syntax.types import *

class Parser:
  def __init__(self, tokenizer, handlers=[]):
    self.current_level = 0
    self.tokenizer = tokenizer
    self.handlers = handlers
    self.token = None
    self.nxtoken = None
    self.is_first_token = True
    self.exit_level_flag = False

  def consume(self):
    if self.token == EOFToken:
      return EOFToken
    
    if self.is_first_token:
      self.token = self.tokenizer.next_token()
      self.is_first_token = False
    else:
      self.token = self.nxtoken
    
    self.nxtoken = self.tokenizer.next_token()

    return self
  
  def expect(self, token_category, token_type):
    if self.nxtoken.category == token_category and self.nxtoken.type == token_type:
      self.consume()
    else:
      self.syntax_error()

  def syntax_error():
    self.tokenizer.unexpected_token()

  def expression(self):
    return self.logical_or_expression()
  
  def logical_or_expression(self):
    expr = self.logical_and_expression()
    while self.nxtoken.value == 'or':
      self.consume()
      operator = self.token
      right = self.logical_and_expression()
      expr = BinaryExpression(expr, operator, right)
    return expr
  
  def logical_and_expression(self):
    return self.equality_expression()
  
  def equality_expression(self):
    expr = self.relational_expression()
    while self.nxtoken.value == '==' or self.nxtoken.value == '!=':
      self.consume()
      operator = self.token
      right = self.relational_expression()
      expr = BinaryExpression(expr, operator, right)
    return expr
  
  def relational_expression(self):
    expr = self.additive_expression()
    while self.nxtoken.value == '>' or self.nxtoken.value == '<' or self.nxtoken.value == '>=' or self.token.value == '<=':
      self.consume()
      operator = self.token
      right = self.additive_expression()
      expr = BinaryExpression(expr, operator, right)
    return expr
  
  def additive_expression(self):
    expr = self.multiplicative_expression()
    while self.nxtoken.value == '+' or self.nxtoken.value == '-':
      self.consume()
      operator = self.token
      right = self.multiplicative_expression()
      expr = BinaryExpression(expr, operator, right)
    return expr

  def multiplicative_expression(self):
    expr = self.unary_expression()
    while self.nxtoken.value == '*' or self.nxtoken.value == '/' or self.nxtoken.value == '%':
      self.consume()
      operator = self.token
      right = self.unary_expression()
      expr = BinaryExpression(expr, operator, right)
    return expr

  def unary_expression(self):
    if self.nxtoken.value == '!' or self.nxtoken.value == '-':
      self.consume()
      operator = self.token
      right = self.unary_expression()
      expr = UnaryExpression(operator, right)
      return expr
    
    return self.primary()
        
  
  def primary(self):
    expr = None
    if self.token == EOFToken:
      return expr

    if self.nxtoken.category == 'literal':
      self.consume()
      return LiteralExpression(self.token)
    elif self.nxtoken.category == 'id':
      self.consume()
      return IdentifierExpression(self.token)
    elif self.nxtoken.value == '(':
      self.consume()
      expr = GroupingExpression(self.expression())
      if self.nxtoken.value != ')':
        self.tokenizer.unexpected_token()
      self.consume()
      return expr
    
    if not self.tokenizer.is_eof():
      self.tokenizer.unexpected_token()
    
    return expr
    

  def parse(self, parent=None):
    statements = []
    statement = None

    self.consume()

    while self.token != EOFToken:
      for parser in self.handlers:
        if parser.is_parsable(self):
          statement = parser.parse(self, parent)
          if self.exit_level_flag:
            self.exit_level_flag = False
            return statements
          if statement is not None:
            statement.next = None
            stmtlen = len(statements)
            
            if stmtlen > 0:
              last_statement = statements[stmtlen - 1]
              last_statement.next = statement
              statement.previous = last_statement
            else:
              statement.previous = None

            statements.append(statement)
      
      statement = None
      self.consume()
      #expression statement here
        
    return statements

  def statement(self):
    statements = self.parse()
    if self.current_level != 0:
      print("syntax error: invalid end")
      exit(0)
    return statements
  




