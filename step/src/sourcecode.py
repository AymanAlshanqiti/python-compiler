EOFCharacter = object()

# src.step().step().back().
class SourceCode:
  def __init__(self, src):
    self.line_number = 1
    self.position = -1
    self.src = src
    self.length = len(self.src)
   
  def is_eof(self):
    return self.position >= self.length 
  
  def is_peekable(self):
    return (self.position + 1) < self.length
  
  def character(self):
    if not self.is_eof() and self.position > -1:
      return self.src[self.position]
    else:
      return EOFCharacter
  
  def peek(self):
    if self.is_peekable():
      return self.src[self.position + 1]
    return EOFCharacter
  
  def nxcharacter(self):
    if self.is_peekable():
      self.position += 1
      if self.character() == '\n':
        self.line_number += 1
      return self.src[self.position]
    return EOFCharacter

  def step(self):
    if not self.is_peekable():
      return EOFCharacter
    self.position += 1
    return self
  
  def back(self):
    if self.position > -1:
      self.position -= 1
    return self
  
  def snapshot(self):
    return {
      'character' : self.character(),
      'line_number': self.line_number,
      'position': self.position
    }

  def reset(self):
    self.line_number = 1
    self.position = -1
    return self

  def __iter__(self):
    return self

  def __next__(self):
    character = self.step().character()
    if character == EOFCharacter:
      raise StopIteration
    return character