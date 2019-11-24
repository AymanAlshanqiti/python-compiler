from tokenizer import Tokenizer
from token import Token
from token_handler import *


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

code = """
$val = 10;
# check $val value
if ($val = 75){
  print($val);
}

function sort_list($array, $sort_handler){
  return $sort_handler($array);
}"""


php_tokenizer_handlers = [
  WhitespaceTokenHandler(), 
  VariableTokenHandler(), 
  NumberTokenHandler(),
  OneCharacterTokenHandler(),
  IdTokenHandler(),
  CommentTokenHandler(),
]

def token_highlighter(token):
  html = ''
  if token.type in sky_style.keys():
    html += '<span style="' + sky_style[token.type]['style'] +';">' + token.value + '</span>'
  else:
    html += '<span style="color:'+ sky_style['default']['style'] +';">' + token.value + '</span>'
  return html


def php_highlighter(php_code, php_style):
  php_tokenizer = Tokenizer(code, php_tokenizer_handlers)
  html_output = "<html><body style='font-size: 18px;'><pre><code padding-bottom: 4px;>"
  for token in php_tokenizer:
    html_output += token.to(token_highlighter)
  html_output += "</code></pre></body></html>"
  return html_output


php_result = php_highlighter(code, sky_style)

with open('file4.html', 'w') as f4:
  f4.write(php_result)
