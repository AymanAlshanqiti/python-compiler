class SymtEntry:
  def __init__(self, name, type, attributes ={}):
    self.name = name
    self.type = type
    self.attributes = attributes
    pass


class SymbolTable:
  def __init__(self,parent=None, children=[]):
    self.entries = {}
    self.parent = parent
    self.children = children
  
  def insert(self, entry):
    self.entries[entry.name] = entry
  
  def lookup(self, name):
    return self.entries.get(name, None)