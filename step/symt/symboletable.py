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
    parent_symt = self
    entry = self.entries.get(name, None)
    if entry != None:
      return entry
    
    parent_symt = parent_symt.parent
    while parent_symt != None:
      entry = parent_symt.entries.get(name, None)
      if entry != None:
        return entry
      
      parent_symt = parent_symt.parent
    
    return None
  
  def assert_duplication(self, symbol_name):
    entry = self.symt.lookup(symbol_name)
    if entry != None:
      print('Error: duplicated parameter "' + symbol_name + '"')
      exit(0)

