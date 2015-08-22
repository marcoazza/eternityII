from collections import deque
class Tile:
  CENTRAL = 0
  BORDER = 1
  CORNER = 2

  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3

  UPLEFT = 0
  UPRIGHT = 1
  DOWNRIGHT = 2
  DOWNLEFT = 3


  def __init__(self,up=None,right=None,down=None,left=None,tile_type=None):
    self.pieces = deque([up,right,down,left])
    self.tile_type = tile_type
    self.row = None
    self.col = None


  def __deepcopy__(self,memo):
    t = self.__class__()
    t.__dict__.update(self.__dict__)
    t.pieces = deque(self.pieces)
    return t

  def rotate(self):
    self.pieces.rotate(1)


class BorderTile(Tile):
  pos_map = { 0 : Tile.UP,
              1 : Tile.RIGHT,
              2 : Tile.DOWN,
              3 : Tile.LEFT }

  def __init__(self,**kwargs):
    Tile.__init__(self,**kwargs)
    for i,e in enumerate(self.pieces):
      if e == 0:
        self.pos = BorderTile.pos_map[i]


  def rotate(self):
    self.pieces.rotate(1)
    self.pos = (self.pos + 1) % 4

class CornerTile(Tile):
  def __init__(self,**kwargs):
    Tile.__init__(self,**kwargs)
    corner_map = {
    (self.pieces[Tile.UP],self.pieces[Tile.RIGHT]) : Tile.UPRIGHT,
    (self.pieces[Tile.RIGHT],self.pieces[Tile.DOWN]) : Tile.DOWNRIGHT,
    (self.pieces[Tile.DOWN],self.pieces[Tile.LEFT]) : Tile.DOWNLEFT,
    (self.pieces[Tile.LEFT],self.pieces[Tile.UP]) : Tile.UPLEFT,
    }
    self.pos = corner_map.get((0,0))


  def rotate(self):
    self.pieces.rotate(1)
    self.pos = (self.pos + 1) % 4









