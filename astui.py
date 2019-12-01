from tkinter import *
from parser import *

class UINodeStyle:
  def __init__(self, shape = "rectangle", fgcolor="black", bgcolor="white", outlinecolor="black", padding= 8, outlinewidth="2"):
    self.shape = shape
    self.fgcolor = fgcolor
    self.bgcolor = bgcolor
    self.outlinecolor = outlinecolor
    self.padding = padding
    self.outlinewidth = outlinewidth
    
class UINode:
  def __init__(self):
    self.node_id = -1
    self.parent_connector_id = -1
    self.children_connector_id = -1
    pass

  def draw_node(self, canvas, x, y, text, uinodestyle):
    text_id = canvas.create_text(x,y, text=text, fill=uinodestyle.fgcolor)
    bounds = canvas.bbox(text_id) 
    if uinodestyle.shape.lower() == 'oval':
      self.node_id = canvas.create_oval(bounds[0] - uinodestyle.padding, bounds[1] - uinodestyle.padding, bounds[2] + uinodestyle.padding, bounds[3] + uinodestyle.padding, fill=uinodestyle.bgcolor, outline=uinodestyle.outlinecolor, width=uinodestyle.outlinewidth)
    else:
      self.node_id = canvas.create_rectangle(bounds[0] - uinodestyle.padding, bounds[1] - uinodestyle.padding, bounds[2] + uinodestyle.padding, bounds[3] + uinodestyle.padding, fill=uinodestyle.bgcolor, outline=uinodestyle.outlinecolor, width=uinodestyle.outlinewidth)

    canvas.tag_lower(self.node_id)
    return self.node_id
  
  def draw_node_connector(self, canvas, node_id, has_parent=True, has_children=True, connector_size = 16, connector_shape="rectangle", fill="white", outline="black", width="2"):
    bounds = canvas.bbox(node_id)

    rwidth = bounds[2] - bounds[0]
    rheight = bounds[3] - bounds[1]

    if has_parent:
      parent_b0 = bounds[2] - (rwidth / 2) - (connector_size / 2)
      parent_b1 = bounds[1] - (connector_size + 2) 
      parent_b2 = parent_b0 + connector_size
      parent_b3 = parent_b1 + connector_size
      if connector_shape.lower() == 'oval':
        self.parent_connector_id = canvas.create_oval(parent_b0, parent_b1, parent_b2, parent_b3, fill=fill, outline=outline, width=width)
      else:
        self.parent_connector_id = canvas.create_rectangle(parent_b0, parent_b1, parent_b2, parent_b3, fill=fill, outline=outline, width=width)
      
    if has_children:
      children_b0 = bounds[2] - (rwidth / 2) - (connector_size / 2)
      children_b1 = bounds[3] + 2
      children_b2 =  bounds[2] - (rwidth / 2) - (connector_size / 2) + connector_size
      children_b3 = children_b1 + connector_size
      
      if connector_shape.lower() == 'oval':
        self.children_connector_id = canvas.create_oval(children_b0, children_b1, children_b2, children_b3, fill=fill, outline=outline, width=width)
      else:
        self.children_connector_id = canvas.create_rectangle(children_b0, children_b1, children_b2, children_b3, fill=fill, outline=outline, width=width)
    
  def draw_line(self, canvas, from_bounds, to_bounds):
    if from_bounds is not None and to_bounds is not None:
      from_width = (from_bounds[2] - from_bounds[0]) / 2
      from_height = (from_bounds[3] - from_bounds[1]) / 2

      to_width = (to_bounds[2] - to_bounds[0]) / 2
      to_height = (to_bounds[3] - to_bounds[1]) / 2
      lnk = canvas.create_line(from_bounds[0] + from_width, from_bounds[1] + from_height, to_bounds[0] + to_width , to_bounds[1] + to_height, fill="black", width="2")
      canvas.tag_lower(lnk)


class UIIdentifierExpression(UINode):
  def __init__(self, idexpression):
    self.expression = idexpression
  
  def draw_node(self, canvas, x, y, uinodestyle):
    super().draw_node(canvas, x, y, self.expression.value, uinodestyle)
    self.draw_node_connector(canvas,self.node_id, True, False, 16, 'oval', '#9cf8ff')


class UILiteralExpression(UINode):
  def __init__(self, literalexpression):
    self.expression = literalexpression
  
  def draw_node(self, canvas, x, y, uinodestyle):
    super().draw_node(canvas, x, y, self.expression.value, UINodeStyle('rectangle', '#000000', '#e8ce05','#e8ce05',16))
    self.draw_node_connector(canvas,self.node_id, True, False, 16, 'oval','#fff7b5')


class UIBinaryExpression(UINode):
  def __init__(self, binaryexpression):
    self.expression = binaryexpression
  
  def draw_node(self, canvas, x, y, uinodestyle):
    self.draw_expression(canvas, x, y, self.expression, 1, uinodestyle)
  
  def draw_expression(self, canvas, x, y, expression, level, uinodestyle, bound=None):
    if isinstance(expression, BinaryExpression):
      super().draw_node(canvas, x , y, expression.operator.value, UINodeStyle('oval', 'white', '#22d49b','#22d49b',16))
      self.draw_node_connector(canvas,self.node_id, True, True, 16, 'oval', '#b3ffe7')

      ###### Begin draw line
      parent_connector_bounds = canvas.bbox(self.parent_connector_id)
      children_connector_bounds = canvas.bbox(self.children_connector_id)

      self.draw_line(canvas, bound, parent_connector_bounds)
      ###### End draw line
      
      self.draw_expression(canvas, x - (50 * level), y + 150, expression.left_expression, level + 1, uinodestyle, children_connector_bounds)
      self.draw_expression(canvas, x + (50 * (level)), y + 150, expression.right_expression, level + 1, uinodestyle, children_connector_bounds)
    elif isinstance(expression, LiteralExpression):
      lexpr = UILiteralExpression(expression)
      lexpr.draw_node(canvas,x, y , uinodestyle)
      ###### Begin draw line
      parent_connector_bounds = canvas.bbox(lexpr.parent_connector_id)
      self.draw_line(canvas, bound, parent_connector_bounds)
      ###### End draw line
    elif isinstance(expression, IdentifierExpression):
      idexpr = UIIdentifierExpression(expression)
      idexpr.draw_node(canvas, x, y , UINodeStyle('rectangle', 'black','#2de0ed','#2de0ed'))
      ###### Begin draw line
      parent_connector_bounds = canvas.bbox(idexpr.parent_connector_id)
      self.draw_line(canvas, bound, parent_connector_bounds)
      ###### End draw line