from abc import ABC, abstractclassmethod

class Node:
  def __init__(self, level=0):
    self.level = level

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
  def __init__(self, token=None, level=0, parent_stmt=None, next_stmt=None,previous_stmt=None, statements=[]):
    super().__init__(token, level, parent_stmt, next_stmt,previous_stmt)
    self.statements = statements

class BinaryExpression(Expression):
  def __init__(self, left, operator, right, level=0):
    super().__init__(level)
    self.left_expression = left
    self.operator = operator
    self.right_expression = right

    self.left_expression.level = level + 1
    self.right_expression.level = level + 1


class UnaryExpression(Expression):
  def __init__(self, operator, expression, level=0):
    super().__init__(level)
    self.expression = expression
    self.operator = operator

class GroupingExpression(Expression):
  def __init__(self, expression, level=0, group_level=0):
    super().__init__(level)
    self.expression = expression
    self.glevel = group_level

class LiteralExpression(Expression):
  def __init__(self, value=None, level=0):
    super().__init__(level)
    self.value = value

class IdentifierExpression(Expression):
  def __init__(self, value=None, level=0):
    super().__init__(level)
    self.value = value