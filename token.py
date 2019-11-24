class Token:
  def __init__(self):
    self.type = '' # ['variable', 'new_line', 'space', 'number', 'assign', 'semicolon', 'keyword']
    self.value = ''
    self.line_number = 1
    self.position = 0

  def to(self, handler):
    return handler(self)