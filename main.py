from tokenizer import Tokenizer
from token import Token


code = """$val = 10;
echo $val;
if $val = 7 echo 2;"""

sky_style = {
  'keyword':{
    'color': 'blue'
  },
  'number':{
    'color': 'gray'
  },
  'variable':{
    'color': 'red',
    'font-weight': 'bold'
  },
  'space':{
    'color': 'white'
  },
  'assign':{
    'color': 'orange'
  },
  'semicolon':{
    'color': 'orange'
  },
  'new_line':{
    'color': 'orange'
  }
}  



tknizer = Tokenizer(code)

html = "<html><body style='font-size: 18px;'><pre><code padding-bottom: 4px;>"
for token in tknizer:
  html += '<span style="color:'+ sky_style[token.token_type]['color'] +';">' + token.token_value + '</span>'

html += "</code></pre></body></html>"

with open("file1.html","w") as f: