from tokenizer import Tokenizer
from token import Token
from token_handler import *
from parser import *

def style_keyword(token):
  if token.type == 'datatype':
    return 'color: gray'
  elif token.type == 'literal':
    return 'color: blue; font-weight: bold'

  return 'color: blue'

def style_number(token):
  return 'color: red'

def style_default(token):
  return 'color: black'

sky_style = {
  'keyword':{
    'style': 'color:blue; font-weight:bold'
  },
  'comment': {
    'style': 'color:green'
  },
  'id':{
    'style': 'color:black; background-color: yellow;'
  },
  'number':{
    'style': 'color:red'
  },
  'variable':{
    'style': 'color:black'
  },
  'default':{
    'style': 'color:black'
  },
} 

ay_tokenizer_handlers = [
  NumberTokenHandler(),
  OneCharacterTokenHandler(),
  IdTokenHandler(),
  CommentTokenHandler(),
]

with open('code.ay', 'r') as ay:
  code = ay.read(1024)

statements = Parser(Tokenizer(code, ay_tokenizer_handlers)).parse()

def print_statements(statements, level=1):
  for statement in statements:
    print(level * '\t', end='')
    print('-> ')
    print("statement type: " + statement.type)
    if isinstance(statement, BlockNode):
      print_statements(statement.statements, level + 1)
    print("-----------------------------------------")

print_statements(statements)

# def token_highlighter(token):
#   html = ''
#   if token.category == 'keyword':
#     html += '<span style="' + style_keyword(token) +';">' + token.value + '</span>'
#   elif token.category == 'number':
#     html += '<span style="' + style_number(token) +';">' + token.value + '</span>'
#   else:
#     html += '<span style="' + style_default(token) +';">' + token.value + '</span>'

#   return html


# def php_highlighter(php_code, php_style):
#   php_tokenizer = Tokenizer(code, php_tokenizer_handlers)
#   html_output = "<html><body style='font-size: 18px;'><pre><code padding-bottom: 4px;>"
#   for token in php_tokenizer:
#     html_output += token.to(token_highlighter)
#   html_output += "</code></pre></body></html>"
#   return html_output


# php_result = php_highlighter(code, sky_style)

# with open('file.html', 'w') as f4:
#   f4.write(php_result)
