
class Node:
  def __init__(self):
    pass

class Statement(Node):
  def __init__(self, token=None, level=0, parent_stmt=None, next_stmt=None,previous_stmt=None):
    self.token = token
    self.level = level
    self.parent = parent_stmt
    self.next = next_stmt
    self.previous = previous_stmt

class Expression(Node):
  def __init__(self):
    pass

class BlockStatement(Statement):
  def __init__(self, token=None, level=0, parent_stmt=None, next_stmt=None,previous_stmt=None, statements=[]):
    super().__init__(token, level, parent_stmt, next_stmt,previous_stmt)
    self.statements = statements

class BinaryExpression(Expression):
  def __init__(self, left, operator, right):
    super().__init__()
    self.left_expression = left
    self.operator = operator
    self.right_expression = right

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