from step.lex.token import *
from step.lex.tokenizer import *
from step.syntax.types import *

class Parser:
  def __init__(self, tokenizer, symt, handlers=[]):
    self.statement_level = 0
    self.expression_level = 0
    self.expgroup_level = 0
    self.tokenizer = tokenizer
    self.handlers = handlers
    self.token = None
    self.nxtoken = None
    self.is_first_token = True
    self.exit_level_flag = False
    self.symt = symt
    self.current_symt = symt

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
  
  def expect(self, token_category, token_type, token_value=None):
    if self.nxtoken.category == token_category and self.nxtoken.type == token_type:
      if token_value != None and self.nxtoken.value != token_value:
        self.syntax_error()
      self.consume()
      return
    
    self.syntax_error()

  def syntax_error(self):
    self.tokenizer.unexpected_token()

  def expression(self):
    return self.logical_or_expression()
  
  def biexprssion(self, condition, expr_parser):
    expr = expr_parser().evalute()
    while condition(self):
      self.consume()
      operator = self.token
      self.expression_level += 1
      right = expr_parser().evalute()
      expr = BinaryExpression(expr, operator, right, self.expression_level).evalute()
      self.expression_level -= 1
    return expr

  def logical_or_expression(self):
    return self.biexprssion(lambda p: p.nxtoken.value == 'or', self.logical_and_expression)
  
  def logical_and_expression(self):
    return self.biexprssion(lambda p: p.nxtoken.value == 'and', self.equality_expression)
  
  def equality_expression(self):
    return self.biexprssion(lambda p: p.nxtoken.value == '==' or p.nxtoken.value == '!=', self.relational_expression)
  
  def relational_expression(self):
    return self.biexprssion(lambda p: p.nxtoken.value == '>' or p.nxtoken.value == '>=' or p.nxtoken.value == '<' or p.nxtoken.value == '<=', self.additive_expression)
  
  def additive_expression(self):
    return self.biexprssion(lambda p: p.nxtoken.value == '+' or p.nxtoken.value == '-' , self.multiplicative_expression)

  def multiplicative_expression(self):
    return self.biexprssion(lambda p: p.nxtoken.value == '*' or p.nxtoken.value == '/' or p.nxtoken.value == '%' , self.unary_expression)

  def unary_expression(self):
    if self.nxtoken.value == '!' or self.nxtoken.value == '-':
      self.consume()
      operator = self.token
      self.expression_level += 1
      right = self.unary_expression()
      expr = UnaryExpression(operator, right, self.expression_level)
      self.expression_level -= 1
      return expr.evalute()
    
    return self.primary()
        
  
  def primary(self):
    expr = None
    if self.token == EOFToken:
      return expr

    if self.nxtoken.category == 'literal':
      self.consume()
      return LiteralExpression(self.token, self.expression_level).evalute()
    elif self.nxtoken.category == 'id':
      self.consume()
      return IdentifierExpression(self.current_symt, self.token, self.expression_level).evalute()
    elif self.nxtoken.value == '(':
      self.consume()
      self.expgroup_level += 1
      expr = GroupingExpression(self.expression(), self.expression_level, self.expgroup_level).evalute()
      if self.nxtoken.value != ')':
        self.tokenizer.unexpected_token()
      self.consume()
      self.expgroup_level -= 1
      return expr
    
    if not self.tokenizer.is_eof():
      self.tokenizer.unexpected_token()
    
    return expr
    

  def parse(self, parent=None):
    statements = []
    statement = None
    
    if parent != None:
      self.current_symt = parent.symt
    
    self.consume()

    while self.token != EOFToken:
      for parser in self.handlers:
        if parser.is_parsable(self):
          statement = parser.parse(self, parent)
          if self.exit_level_flag: #end
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
    if self.statement_level != 0:
      print("syntax error: invalid end")
      exit(0)
    return statements
  




