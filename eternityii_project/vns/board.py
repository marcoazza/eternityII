from math import sqrt
from tile import BorderTile,CornerTile,Tile
import random
from copy import deepcopy

class BoardCell:
  def __init__(self):
    self.tile = None
    self.match = Tile(up=0,right=0,down=0,left=0)


  def __deepcopy__(self,memo):
    b = BoardCell()
    b.__dict__.update(self.__dict__)
    b.tile = deepcopy(self.tile)
    b.match = deepcopy(self.match)
    return b

class Board:
  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3

  UPLEFT = 0
  UPRIGHT = 1
  DOWNRIGHT = 2
  DOWNLEFT = 3

  def __init__(self):
    self.board_matrix = None
    self.tiles = { 0:[],
                   1:[],
                   2:[],
                   }
    self.N = None
    self.tiles_list = None
    self.score = 0
    self.row_map = None
    self.col_map = None
    self.corner_map = None


  def __deepcopy__(self,memo):
    b = Board()
    b.__dict__.update(self.__dict__)
    b.row_map = self.row_map.copy()
    b.col_map = self.col_map.copy()
    b.corner_map = self.corner_map.copy()
    b.tiles_list = [deepcopy(e) for e in self.tiles_list]
    b.tiles = deepcopy(self.tiles)
    b.board_matrix = deepcopy(self.board_matrix)
    return b


  def init_constants(self):
    self.row_map = { 0: Board.UP,
                     self.N : Board.DOWN,
                     }
    self.col_map = { 0: Board.LEFT,
                     self.N : Board.RIGHT,
                     }
    self.corner_map = {
      (0,self.N-1) : Board.UPRIGHT,
      (self.N-1,self.N-1) : Board.DOWNRIGHT,
      (self.N-1,0) : Board.DOWNLEFT,
      (0,0) : Board.UPLEFT,
      }


  def reset_tiles(self):
    for key,t in self.tiles.items():
      self.tiles[key] = []


  def load_game_file(self,filename):
    tiles = []
    tiles_map = {0: Tile, 1: BorderTile , 2: CornerTile}
    with open(filename) as f:
      for board_tile in f.readlines():
        t = [int(i) for i in board_tile.split()]
        up,right,down,left = t
        pos = t.count(0)
        constr = tiles_map.get(t.count(0))
        tile = constr(up=up,right=right,down=down,left=left,tile_type=pos)
        tiles.append(tile)

    return tiles


  def arrange(self,tiles):
    self.N = int(sqrt(len(tiles)))
    self.init_constants()
    self.tiles_list = tiles
    self.reset_tiles()
    self.board_matrix = [ [BoardCell() for j in range(self.N)] for i in range(self.N)]

    for j,tile in enumerate(tiles):
      self.board_matrix[j/self.N][j%self.N].tile = tile
      self.tiles[tile.tile_type].append(tile)
      tile.row, tile.col = j/self.N , j%self.N

    for tile in tiles:
      self.update_matches(tile)
    self.evaluate_score()

    frame_borders = self.get_borders(self.board_matrix)
    frame_corners = self.get_corners(self.board_matrix)

    random.shuffle(frame_borders)
    random.shuffle(frame_corners)

    for i in range(len(frame_borders)):
      self.swap(self.tiles[1][i],frame_borders[i].tile,complete=False)

    for i in range(len(frame_corners)):
      self.swap(self.tiles[2][i],frame_corners[i].tile,complete=False)


  def get_borders(self,board):
    frame = []
    frame.extend(self.board_matrix[0][1:self.N-1] + self.board_matrix[self.N-1][1:self.N-1])
    for e in self.board_matrix[1:self.N-1]:
      frame.append(e[0])
      frame.append(e[self.N-1])
    return frame


  def get_corners(self,board):
    return [board[0][0],board[0][self.N-1],board[self.N-1][0],board[self.N-1][self.N-1]]


  def get_snapshot(self):
    tiles_list = []
    for i,row in enumerate(self.board_matrix):
      for j,c in enumerate(row):
        tiles_list.append(self.board_matrix[i][j].tile)
    return tiles_list


  def check_tiles(self):
    tiles_map = {}
    for i,row in enumerate(self.board_matrix):
      for j,c in enumerate(row):
        for piece in c.tile.pieces:
          if tiles_map.get(piece) is not None:
            tiles_map[piece] += 1
          else:
            tiles_map[piece] = 1
    print '##### TILES COLORS #####'
    for k,v in tiles_map.items():
      print 'color:{} occurrences: {}'.format(k,v)
    print '\n'*2


  def swap(self,tile1,tile2,complete=True):
    tile1.row ,tile2.row = tile2.row , tile1.row
    tile1.col ,tile2.col = tile2.col , tile1.col

    for t in [tile1,tile2]:
      self.board_matrix[t.row][t.col].tile = t
      self.autorotate(t)
    self.update_matches(tile1)
    self.update_matches(tile2)



  def rotate(self,tile):
    tile.rotate()
    self.update_matches(tile)


  def tile_position(self,tile):
    if isinstance(tile,BorderTile):
      return self.position(tile)
    if isinstance(tile,CornerTile):
      return self.corner_position(tile)


  def autorotate(self,tile):
    new_pos = self.tile_position(tile)
    if new_pos is not None:
      while tile.pos != new_pos :
        tile.rotate()


  def position(self,tile):
    if tile.row == 0:
      return Board.UP
    if tile.row == self.N-1:
      return Board.DOWN
    if tile.col == 0:
      return Board.LEFT
    if tile.col == self.N-1:
      return Board.RIGHT


  def corner_position(self,tile):
    return self.corner_map.get((tile.row,tile.col),None)


  def update_matches(self,tile):
    adj_indexes = self.get_adj_indexes(tile.row,tile.col)
    match_order = [Tile.DOWN,Tile.LEFT,Tile.UP,Tile.RIGHT]

    adj_pieces = []
    for m,i in enumerate(adj_indexes):
      if i is not None:
        adj_pieces.append( self.board_matrix[i[0]][i[1]].tile.pieces[match_order[m]])
      else:
        adj_pieces.append(None)

    for i,t in enumerate(tile.pieces):
      if adj_pieces[i] is not None:
        adj_row, adj_col = adj_indexes[i]
        current_adj = self.board_matrix[adj_row][adj_col].match.pieces[match_order[i]]
        tile_match = self.board_matrix[tile.row][tile.col].match.pieces[i]
        old_adj = (current_adj == 1 and tile_match == 1)
        if t == adj_pieces[i]:
          self.board_matrix[tile.row][tile.col].match.pieces[i] = 1
          self.board_matrix[adj_indexes[i][0]][adj_indexes[i][1]].match.pieces[match_order[i]] = 1
          if not old_adj:
            self.score += 1
        else:
          if old_adj:
            self.score -= 1
          self.board_matrix[tile.row][tile.col].match.pieces[i] = 0
          self.board_matrix[adj_indexes[i][0]][adj_indexes[i][1]].match.pieces[match_order[i]] = 0


  def get_adj_indexes(self,i,j):
    idx_list = [ (i-1,j), (i,j+1), (i+1,j), (i,j-1) ]
    for k,adj in enumerate(idx_list):
      if adj[0] < 0 or adj[0] > self.N -1 or adj[1] < 0 or adj[1] > self.N -1:
        idx_list[k] = None
    return idx_list


  def evaluate_score(self):
    score = 0
    for i,r in enumerate(self.board_matrix):
      for j, t in enumerate(r):
        score += sum(self.board_matrix[i][j].match.pieces)

    score /= 2
    self.score = score
    return score

