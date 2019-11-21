from tokenizer import Tokenizer
from token import Token


code = """$val_6_Welcome = 10;
echo $val;
if $data = 7 echo 2;"""

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
# print(tknizer.source_code)

html = "<html><body style='font-size: 18px;'><pre><code padding-bottom: 4px;>"
for token in tknizer:
  # print(token.token_value)
  html += '<span style="color:'+ sky_style[token.token_type]['color'] +';">' + token.token_value + '</span>'

html += "</code></pre></body></html>"

with open("file1.html","w") as f:
  f.write(html)
  # print('\nThe length of source code is %s characters, and I\'m gonna loop throw it!' % token.length)
  # print('token type: %s' % token.ypte)
  # print('token value: %s' % token.token_value)
  # print('token line number: %s' % token.token_line_number)
  # print('token position: %s' % token.token_position)