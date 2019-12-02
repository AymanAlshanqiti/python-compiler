from token import *
from tokenizer import *
from types import *


class Parser:
  def __init__(self, tokenizer, handlers=[]):
    self.current_level = 0
    self.tokenizer = tokenizer
    self.handlers = handlers

  def syntax_error(self, message, line_number, position):
    print('Ay syntax error:' + message + ', line number : ' + str(line_number) + ', position: ' + str(position))
    exit(0)
  
  def match(self, token_category, token_type):
    self.token = self.tokenizer.next()
    if self.token.category != token_category or self.token.type != token_type:
      self.syntax_error('unexpected token', self.token.line_number, self.token.position)
 
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
  def parse(self, parent=None):
    statements = []
    self.token = self.tokenizer.next()

    while self.token != EOFToken:
      for parser in self.handlers:

        if parser.is_parsable(self):
          statement = parser.parse(self, parent)

        if statement is not None:
          self.attach_statement(parent, statements, statement)
      
      statement = None
      self.token = self.tokenizer.next()

    return statements

  def attach_statement(self, parent, statements, statement):
    statements_len = len(statements)
    if statements_len > 0:
      last_statement = statements[statements_len - 1]
      statement.parent = parent
      statement.next = None
      statement.previous = last_statement
      last_statement.next = statement
      
    statements.append(statement)
    
  def has_error(self):
    return not self.current_level == 0
