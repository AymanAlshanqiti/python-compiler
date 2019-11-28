class Token:
  def __init__(self):
    self.category = '' # ['variable', 'new_line', 'space', 'number', 'assign', 'semicolon', 'keyword']
    self.type = ''
    self.value = ''
    self.line_number = 1
    self.position = 0
    self.data = {}

  def to(self, handler):
    return handler(self)

  def add(self, key, value):
    self.data[key] = value

  def remove(self, key):
    del self.data[key]
  
EOFToken = Token()
EOFToken.category = 'EOF'

ERRToken = Token()
ERRToken.category = 'ERR'
