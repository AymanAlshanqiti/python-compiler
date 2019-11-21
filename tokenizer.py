
class Tokenizer:
  def __init__(self, source_code):
    self.line_number = 1
    self.pointer_position = 0
    self.source_code = source_code
    self.length = len(self.source_code)
    self.keywords = ['if', 'else', 'for', 'echo', 'break', 'while', 'switch']
    self.tokens = []

  # @property
  # def is_eof(self):
  #   return not self.pointer_position < self.source_len
  
  # @property
  # def character(self):
  #   try:
  #     return self.source_code[self.pointer_position]
  #   except:
  #     return None
  
  def read_variable(self, token):
    token.token_line_number = self.line_number
    token.token_position = self.pointer_position
    token.token_type = 'variable'
    token.token_value = self.source_code[self.pointer_position]
    self.pointer_position += 1
    while self.source_code[self.pointer_position].isalnum() or self.source_code[self.pointer_position] == '_':
      token.token_value += self.source_code[self.pointer_position]
      self.pointer_position += 1

  def read_space(self, token):
    if self.source_code[self.pointer_position] == '\n':
      self.line_number += 1
      token.token_type = 'new_line'
    else:
      token.token_type = 'space'
    token.token_line_number = self.line_number
    token.token_position = self.pointer_position
    token.token_value = self.source_code[self.pointer_position]
    self.pointer_position += 1
    while self.source_code[self.pointer_position].isspace():
      token.token_value += self.source_code[self.pointer_position]
      self.pointer_position += 1

  def read_number(self):
    pass

  def read_comments(self):
    pass
  
  def next_token(self):
    if self.character is None:
      return None
    
    if self.is_eof:
      return EofToken

    if self.character.isalpha() or self.character == '_':
      return self.read_id()
    elif self.character == '#':
      return self.read_comments()
    pass

  def go_next(self, character, token):

    if character == '$':
      self.read_variable(token)
      # token.token_line_number = self.line_number
      # token.token_position = self.pointer_position
      # token.token_type = 'variable'
      # token.token_value = self.source_code[self.pointer_position]
      # self.pointer_position += 1
      # while self.source_code[self.pointer_position].isalnum() or self.source_code[self.pointer_position] == '_':
      #   token.token_value += self.source_code[self.pointer_position]
      #   self.pointer_position += 1

    elif character.isspace():
      self.read_space(token)
      # if self.source_code[self.pointer_position] == '\n':
      #   self.line_number += 1
      #   token.token_type = 'new_line'
      # else:
      #   token.token_type = 'space'
      # token.token_line_number = self.line_number
      # token.token_position = self.pointer_position
      # token.token_value = self.source_code[self.pointer_position]
      # self.pointer_position += 1
      # while self.source_code[self.pointer_position].isspace():
      #   token.token_value += self.source_code[self.pointer_position]
      #   self.pointer_position += 1

    elif self.source_code[self.pointer_position].isdigit():
      token.token_type = 'number'
      token.token_value = self.source_code[self.pointer_position]
      self.pointer_position += 1
      token.token_line_number = self.line_number
      token.token_position = self.pointer_position
      while self.source_code[self.pointer_position].isdigit():
        token.token_value += self.source_code[self.pointer_position]
        self.pointer_position += 1

    elif self.source_code[self.pointer_position] == '=':
      token.token_type = 'assign'
      token.token_value = self.source_code[self.pointer_position]
      self.pointer_position += 1
      token.token_line_number = self.line_number
      token.token_position = self.pointer_position

    elif self.source_code[self.pointer_position] == ';':
      token.token_type = 'semicolon'
      token.token_value = self.source_code[self.pointer_position]
      self.pointer_position += 1
      token.token_line_number = self.line_number
      token.token_position = self.pointer_position

    elif self.source_code[self.pointer_position].isalpha():
      token.token_value = self.source_code[self.pointer_position]
      self.pointer_position += 1
      while self.source_code[self.pointer_position].isalpha():
        token.token_value += self.source_code[self.pointer_position]
        self.pointer_position += 1
      if token.token_value in self.keywords:
        token.token_type = 'keyword'

    else:
      print("error: Unexpected token")
      self.pointer_position += 1



class Token:
  def __init__(self):
    self.token_type = '' #['variable', 'new_line', 'space', 'number', 'assign', 'semicolon', 'keyword', 'EOF']
    self.token_value = ''
    self.token_line_number = 1
    self.token_position = 0


# EofToken = Token()
# EofToken.token_type = 'EOF'

code = """$val_6_Welcome = 10;
echo $val;
if $data = 7 echo 2;"""

tknizer = Tokenizer(code)
print('I have created a new Tokenizer obj boss!')
print('The length of source code is %s characters, and I\'m gonna loop throw it!' % tknizer.length)


while tknizer.pointer_position < tknizer.length:
  token = Token()
  tknizer.tokens.append(token)
  tknizer.go_next(tknizer.source_code[tknizer.pointer_position], token)
  # if tknizer.source_code[tknizer.pointer_position] == '$':
  #   token.token_line_number = tknizer.line_number
  #   token.token_position = tknizer.pointer_position
  #   token.token_type = 'variable'
  #   token.token_value = tknizer.source_code[tknizer.pointer_position]
  #   tknizer.pointer_position += 1
  #   while tknizer.source_code[tknizer.pointer_position].isalnum() or tknizer.source_code[tknizer.pointer_position] == '_':
  #     token.token_value += tknizer.source_code[tknizer.pointer_position]
  #     tknizer.pointer_position += 1

  # if tknizer.source_code[tknizer.pointer_position].isspace():
  #   if tknizer.source_code[tknizer.pointer_position] == '\n':
  #     tknizer.line_number += 1
  #     token.token_type = 'new_line'
  #   else:
  #     token.token_type = 'space'
  #   token.token_line_number = tknizer.line_number
  #   token.token_position = tknizer.pointer_position
  #   token.token_value = tknizer.source_code[tknizer.pointer_position]
  #   tknizer.pointer_position += 1
  #   while tknizer.source_code[tknizer.pointer_position].isspace():
  #     token.token_value += tknizer.source_code[tknizer.pointer_position]
  #     tknizer.pointer_position += 1

  # elif tknizer.source_code[tknizer.pointer_position].isdigit():
  #   token.token_type = 'number'
  #   token.token_value = tknizer.source_code[tknizer.pointer_position]
  #   tknizer.pointer_position += 1
  #   token.token_line_number = tknizer.line_number
  #   token.token_position = tknizer.pointer_position
  #   while tknizer.source_code[tknizer.pointer_position].isdigit():
  #     token.token_value += tknizer.source_code[tknizer.pointer_position]
  #     tknizer.pointer_position += 1

  # elif tknizer.source_code[tknizer.pointer_position] == '=':
  #   token.token_type = 'assign'
  #   token.token_value = tknizer.source_code[tknizer.pointer_position]
  #   tknizer.pointer_position += 1
  #   token.token_line_number = tknizer.line_number
  #   token.token_position = tknizer.pointer_position

  # elif tknizer.source_code[tknizer.pointer_position] == ';':
  #   token.token_type = 'semicolon'
  #   token.token_value = tknizer.source_code[tknizer.pointer_position]
  #   tknizer.pointer_position += 1
  #   token.token_line_number = tknizer.line_number
  #   token.token_position = tknizer.pointer_position

  # elif tknizer.source_code[tknizer.pointer_position].isalpha():
  #   token.token_value = tknizer.source_code[tknizer.pointer_position]
  #   tknizer.pointer_position += 1
  #   while tknizer.source_code[tknizer.pointer_position].isalpha():
  #     token.token_value += tknizer.source_code[tknizer.pointer_position]
  #     tknizer.pointer_position += 1
  #   if token.token_value in tknizer.keywords:
  #     token.token_type = 'keyword'

  # else:
  #   print("error: Unexpected token")
  #   tknizer.pointer_position += 1

print("loool", tknizer.tokens[4].token_value)