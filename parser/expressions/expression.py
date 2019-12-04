class BinaryExpression(Expression):
  def __init__(self, left, operator, right):
    super().__init__()
    self.left_expression = left
    self.operator = operator
    self.right_expression = right

class UnaryExpression(Expression):
  def __init__(self, operator, expression):
    super().__init__()
    self.expression = expression
    self.operator = operator

class GroupingExpression(Expression):
  def __init__(self, expression):
    super().__init__()
    self.expression = expression

class LiteralExpression(Expression):
  def __init__(self, value=None):
    super().__init__()
    self.value = value

class IdentifierExpression(Expression):
  def __init__(self, value=None):
    super().__init__()
    self.value = value