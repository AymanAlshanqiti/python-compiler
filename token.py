class Token:
  def __init__(self):
    self.token_type = '' # ['variable', 'new_line', 'space', 'number', 'assign', 'semicolon', 'keyword']
    self.token_value = ''
    self.token_line_number = 1
    self.token_position = 0