from abc import ABC, abstractclassmethod

class ParserHandler(ABC):
  def __init__(self):
    pass
  
  @abstractclassmethod
  def is_parsable(self, parser):
    return False

  @abstractclassmethod
  def parse(self, parser, parent=None):
    return None