from color import Color

class TileGUI:
  def_size = 50
  def __init__(self,board,x1,y1,x2,y2,size=0):
    self.up = board.create_polygon(x1, y1,x1+size/2,y1+size/2, x2, y1,outline='black',fill='red')
    self.left = board.create_polygon(x1, y1,x1+size/2,y1+size/2, x1, y2,outline='black',fill='yellow')
    self.right = board.create_polygon(x2, y1,x1+size/2,y1+size/2, x2, y2,outline='black',fill='green')
    self.down = board.create_polygon(x1, y2,x1+size/2,y1+size/2, x2, y2,outline='black',fill='blue')
    self.board = board

  def configure(self,up=Color.color,right=Color.color,down=Color.color,left=Color.color):
    self.board.itemconfig(self.up,fill=Color.color(col=up))
    self.board.itemconfig(self.right,fill=Color.color(col=right))
    self.board.itemconfig(self.down,fill=Color.color(col=down))
    self.board.itemconfig(self.left,fill=Color.color(col=left))
