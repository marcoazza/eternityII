from math import sqrt
from tile import BorderTile,CornerTile,Tile
import random


class BoardCell:
  def __init__(self):
    self.tile = None
    self.rotations = None
    self.match = Tile(up=0,right=0,down=0,left=0)
    self.score = 0

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

  def arrange(self,tiles):
    self.N = int(sqrt(len(tiles)))
    self.init_constants()
    self.tiles_list = tiles
    self.board_matrix = [ [BoardCell() for j in range(self.N)] for i in range(self.N)]
    j = 0
    for tile in tiles:
      self.board_matrix[j/self.N][j%self.N].tile = tile
      self.tiles[tile.tile_type].append(tile)
      tile.row, tile.col = j/self.N , j%self.N
      j += 1

    frame_borders = self.get_borders(self.board_matrix)
    frame_corners = self.get_corners(self.board_matrix)

    random.shuffle(frame_borders)
    random.shuffle(frame_corners)

    for i in range(len(frame_borders)):
      self.swap(self.tiles[1][i],frame_borders[i].tile)

    for i in range(len(frame_corners)):
      self.swap(self.tiles[2][i],frame_corners[i].tile)


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


  def swap(self,tile1,tile2):
    tile1.row ,tile2.row = tile2.row , tile1.row
    tile1.col ,tile2.col = tile2.col , tile1.col

    for t in [tile1,tile2]:
      self.board_matrix[t.row][t.col].tile = t
      if isinstance(t,BorderTile):
        self.autorotate_border(t)
      if isinstance(t,CornerTile):
        self.autorotate_corner(t)

    self.update_matches(tile1)
    self.update_matches(tile2)
    self.evaluate_score()


  def rotate(self,tile):
    tile.rotate()
    self.update_matches(tile)
    self.evaluate_score()

  def autorotate_border(self,tile):
    new_pos = self.position(tile)
    if new_pos is not None:
      while tile.border_pos != new_pos :
        tile.rotate()

  def autorotate_corner(self,tile):
    new_pos = self.corner_position(tile)
    if new_pos is not None:
      i = 0
      while tile.corner_pos != new_pos and i < 4:
        tile.rotate()
        i += 1

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
        adj_pieces.append( self.board_matrix[i[0]][i[1]].tile.pieces[match_order[m]] )
      else:
        adj_pieces.append(None)

    for i,t in enumerate(tile.pieces):
      if adj_pieces[i] is not None:
        if t == adj_pieces[i]:
          self.board_matrix[tile.row][tile.col].match.pieces[i] = 1
          self.board_matrix[tile.row][tile.col].score += 1
          self.board_matrix[adj_indexes[i][0]][adj_indexes[i][1]].match.pieces[match_order[i]] = 1
          self.board_matrix[adj_indexes[i][0]][adj_indexes[i][1]].score += 1
        else:
          self.board_matrix[tile.row][tile.col].match.pieces[i] = 0
          self.board_matrix[tile.row][tile.col].score = 0
          self.board_matrix[adj_indexes[i][0]][adj_indexes[i][1]].match.pieces[match_order[i]] = 0
          self.board_matrix[adj_indexes[i][0]][adj_indexes[i][1]].score = 0

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



