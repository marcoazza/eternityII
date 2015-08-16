from collections import deque

class Tile:
  CENTRAL = 0
  BORDER = 1
  CORNER = 2

  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3

  t_map = { 0 : UP,
            1 : RIGHT,
            2 : DOWN,
            3 : LEFT
  }
  UPLEFT = 0
  UPRIGHT = 1
  DOWNRIGHT = 2
  DOWNLEFT = 3


  def __init__(self,up=None,right=None,down=None,left=None,tile_type=None):
    self.pieces = deque([up,right,down,left])
    self.tile_type = tile_type
    self.row = None
    self.col = None


  def rotate(self):
    self.pieces.rotate(1)


  def __repr__(self):
    return '{}-{}-{}-{} r:{} c:{}'.format(self.pieces[Tile.UP],
                                          self.pieces[Tile.RIGHT],
                                          self.pieces[Tile.DOWN],
                                          self.pieces[Tile.LEFT],
                                          self.row,
                                          self.col)





class BorderTile(Tile):
  pos_map = { 0 : Tile.t_map[0],
              1 : Tile.t_map[1],
              2 : Tile.t_map[2],
              3 : Tile.t_map[3] }

  def __init__(self,**kwargs):
    Tile.__init__(self,**kwargs)
    i = 0
    for e in self.pieces:
      if e == 0:
        self.border_pos = BorderTile.pos_map[i]
      i += 1

  def rotate(self):
    self.pieces.rotate(1)
    self.border_pos = (self.border_pos + 1) % 4

class CornerTile(Tile):
  def __init__(self,**kwargs):
    Tile.__init__(self,**kwargs)
    corner_map = {
    (self.pieces[Tile.UP],self.pieces[Tile.RIGHT]) : Tile.UPRIGHT,
    (self.pieces[Tile.RIGHT],self.pieces[Tile.DOWN]) : Tile.DOWNRIGHT,
    (self.pieces[Tile.DOWN],self.pieces[Tile.LEFT]) : Tile.DOWNLEFT,
    (self.pieces[Tile.LEFT],self.pieces[Tile.UP]) : Tile.UPLEFT,
    }
    self.corner_pos = corner_map.get((0,0))


  def rotate(self):
    self.pieces.rotate(1)
    self.corner_pos = (self.corner_pos + 1) % 4









