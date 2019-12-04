class Token:
  def __init__(self, category=None, ttype=None, value=None, line_number=1, position=0):
    self.category = category
    self.type = ttype
    self.value = value
    self.line_number = line_number
    self.position = position
    self.metadata = {}
  
  def add_metadata(self, key, value):
    self.metadata[key] = value



EOFToken = Token()
EOFToken.category = 'EOF'
EOFToken.type = 'eof'
EOFToken.value = 'eof'

ERRToken = Token()
ERRToken.category = 'ERR'
