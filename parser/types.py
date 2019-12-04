from abc import ABC, abstractclassmethod

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


class ExpressionParserHandler(ABC):
  def __init__(self, tokenizer):
    self.tokenizer = tokenizer
    pass

  @abstractclassmethod
  def expression(self):
    return None