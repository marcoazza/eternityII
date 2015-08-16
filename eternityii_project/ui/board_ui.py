try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

from math import sqrt
from tile_gui import TileGUI

class BoardGUI:
  def __init__(self,master,**kwargs):
    self.canvas = tk.Canvas(master, **kwargs)
    self.canvas.pack()
    self.width = kwargs.get('width',None)
    self.height = kwargs.get('width',None)
    self.tiles = None
    #self.load_board('../end.txt')


  def load_board(self,filename):
    with open(filename,'r') as board_file:
      lines  = board_file.readlines()
      self.N = int(sqrt(len(lines)))
      self.canvas.configure(width=TileGUI.def_size*self.N,height=TileGUI.def_size*self.N)
      self.width = TileGUI.def_size*self.N
      self.height = TileGUI.def_size*self.N
      self.L = self.width/self.N
      if not self.N**2 == len(lines):
        raise Exception

      self.tiles = [ [None for j in range(self.N)] for i in range(self.N)]
      row = 0
      for i in range(0, self.width, self.L):
          y1, y2 = i, i + self.L
          col = 0
          for j in range(0, self.height, self.L):
              x1, x2 = j, j + self.L
              self.tiles[row][col] = TileGUI(self.canvas,x1,y1,x2,y2,size=self.L)
              col+=1
          row+=1

      #setup colors
      j = 0
      for board_tile in lines:
        up,right,down,left = [int(i) for i in board_tile.split()]
        self.tiles[j/self.N][j%self.N].configure(up=up,right=right,down=down,left=left)
        j += 1



  def update_board(self,tiles):
      j = 0
      for board_tile in tiles:
        up,right,down,left = board_tile.pieces
        self.tiles[j/self.N][j%self.N].configure(up=up,right=right,down=down,left=left)
        j += 1




