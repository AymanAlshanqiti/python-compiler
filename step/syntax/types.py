from abc import ABC, abstractclassmethod
from step.symt.symboletable import *

class Node:
  def __init__(self, level=0):
    self.level = level
    self.gattrs = {} # attribute grammar (context-sensitive analysis)

class Statement(Node):
  def __init__(self, token=None, level=0, parent_stmt=None, next_stmt=None,previous_stmt=None):
    super().__init__(level)
    self.token = token
    self.parent = parent_stmt
    self.next = next_stmt
    self.previous = previous_stmt

class Expression(Node):
  def __init__(self, level=0):
    super().__init__(level)

class BlockStatement(Statement):
  def __init__(self,parent_symt, token=None, statements=[], level=0, parent_stmt=None, next_stmt=None,previous_stmt=None):
    super().__init__(token, level, parent_stmt, next_stmt,previous_stmt)
    self.statements = statements
    self.symt = SymbolTable(parent_symt)

class BinaryExpression(Expression):
  def __init__(self, left, operator, right, level=0):
    super().__init__(level)
    self.left_expression = left
    self.operator = operator
    self.right_expression = right

    self.left_expression.level = level + 1
    self.right_expression.level = level + 1
  
  def evalute(self):
    if self.operator.value == '+':
      self.gattrs['value'] = self.left_expression.gattrs['value'] + self.right_expression.gattrs['value']
    elif self.operator.value == '-':
      self.gattrs['value'] = self.left_expression.gattrs['value'] - self.right_expression.gattrs['value']
    elif self.operator.value == '*':
      self.gattrs['value'] = self.left_expression.gattrs['value'] * self.right_expression.gattrs['value']
    elif self.operator.value == '/':
      self.gattrs['value'] = self.left_expression.gattrs['value'] / self.right_expression.gattrs['value']

    return self


class UnaryExpression(Expression):
  def __init__(self, operator, expression, level=0):
    super().__init__(level)
    self.expression = expression
    self.expression.level = level + 1
    self.operator = operator
  
  def evalute(self):
    if self.operator.value == '-':
      self.gattrs['value'] = -1 * self.expression.gattrs['value']
    elif self.operator.value == '!':
      self.gattrs['value'] = not self.expression.gattrs['value']
    return self

class GroupingExpression(Expression):
  def __init__(self, expression, level=0, group_level=0):
    super().__init__(level)
    self.expression = expression
    self.glevel = group_level
  
  def evalute(self):
    self.gattrs['value'] = self.expression.gattrs['value']
    return self

class LiteralExpression(Expression):
  def __init__(self, value=None, level=0):
    super().__init__(level)
    self.value = value
  
  def evalute(self):
    if self.value.metadata['datatype'] == 'integer':
      self.gattrs['value'] = int(self.value.value)
    elif self.value.metadata['datatype'] == 'float':
      self.gattrs['value'] = float(self.value.value)
    elif self.value.metadata['datatype'] == 'boolean':
      if self.value.value == 'true':
        self.gattrs['value'] = True
      else:
        self.gattrs['value'] = False
    return self

class IdentifierExpression(Expression):
  def __init__(self, value=None, level=0):
    super().__init__(level)
    self.value = value
  
  def evalute(self):
    self.gattrs['value'] = 1
    return self