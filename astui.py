from tkinter import *

canvas_width = 500
canvas_height = 500
canvas_center_x = canvas_width / 2
canvas_center_y = canvas_height / 2
rpadding = 16
master = Tk()

w = Canvas(master, width=canvas_width, height=canvas_height)
w.pack()

def draw_node(canvas, x, y, text,type='rectangle', rpadding =32, text_color="black", fill="white", outline="white", outlinewidth="2"):
  text_id = canvas.create_text(x,y, text=text, fill=text_color)
  bounds = canvas.bbox(text_id)  # returns a tuple like (x1, y1, x2, y2)
  if type.lower() == 'rectangle':
    node_id = canvas.create_rectangle(bounds[0] - rpadding, bounds[1] - rpadding, bounds[2] + rpadding, bounds[3] + rpadding, fill=fill, outline=outline, width=outlinewidth)
  else:
    node_id = canvas.create_oval(bounds[0] - rpadding, bounds[1] - rpadding, bounds[2] + rpadding, bounds[3] + rpadding, fill=fill, outline=outline, width=outlinewidth)

  canvas.tag_lower(node_id)
  return node_id

node_id = draw_node(w, 240, 100, 'Ayman++ Programming Language -> data','rectangle', rpadding, "white", "blue", "blue")
bounds = w.bbox(node_id)

rsize = 32
rwidth = bounds[2] - bounds[0]
rheight = bounds[3] - bounds[1]

parent_b0 = bounds[2] - (rwidth / 2) - (rsize / 2)
parent_b1 = bounds[1] - (rsize + 2) 
parent_b2 = parent_b0 + rsize
parent_b3 = parent_b1 + rsize

children_b0 = bounds[2] - (rwidth / 2) - (rsize / 2)
children_b1 = bounds[3] + 2
children_b2 = parent_b0 + rsize
children_b3 = children_b1 + rsize

r = w.create_oval(parent_b0, parent_b1, parent_b2, parent_b3, fill="white", outline="blue", width="4")
r = w.create_oval(children_b0, children_b1, children_b2, children_b3, fill="white", outline="blue", width="4")

parent_from_x = children_b0 + (rsize / 2)
parent_from_y = children_b1 + (rsize / 2)
#second node

node_id = draw_node(w, bounds[0], 200, 'if','oval', rpadding, "black", "yellow", "yellow")
bounds = w.bbox(node_id)

rwidth = bounds[2] - bounds[0]
rheight = bounds[3] - bounds[1]

parent_b0 = bounds[2] - (rwidth / 2) - (rsize / 2)
parent_b1 = bounds[1] - (rsize / 2)
parent_b2 = parent_b0 + rsize
parent_b3 = parent_b1 + rsize

children_b0 = bounds[2] - (rwidth / 2) - (rsize / 2)
children_b1 = bounds[3] - (rsize / 2)
children_b2 = parent_b0 + rsize
children_b3 = bounds[3] + (rsize / 2)

r = w.create_oval(parent_b0, parent_b1, parent_b2, parent_b3, fill="white", outline="blue", width="4")
r = w.create_oval(children_b0, children_b1, children_b2, children_b3, fill="white", outline="blue", width="4")

children_from_x = parent_b0 + (rsize / 2)
children_from_y = parent_b1 + (rsize / 2)

lnk = w.create_line(parent_from_x, parent_from_y, children_from_x , children_from_y, fill="black", width="2")
w.tag_lower(lnk)



mainloop()