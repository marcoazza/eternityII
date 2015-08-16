from board import Board
from tile import Tile, BorderTile, CornerTile
import random
from copy import deepcopy
from steepest_descent import SteepestDescent
from math import sqrt



class VNS:
  def __init__(self):
    self.current = Board()
    self.best = Board()
    random.seed()
    self.k = 1
    self.k_max = None
    self.max_score = None
    self.N = 0
    self.local_search = SteepestDescent()


    self.chances = {
      Tile.CENTRAL : 0.0,
      Tile.BORDER : 0.0,
      Tile.CORNER : 0.0,
    }

    self.prob_map = {
      Tile.CENTRAL : 0.0,
      Tile.BORDER : 0.0,
      Tile.CORNER : 0.0,
    }
    self.total = 25.0


  def load_game_file(self,filename):
    with open(filename) as f:
      tiles = []
      for board_tile in f.readlines():
        t = [int(i) for i in board_tile.split()]
        up,right,down,left = t
        pos = t.count(0)
        tile = None
        if pos == Tile.BORDER:
          tile = BorderTile(up=up,right=right,down=down,left=left,tile_type=pos)
        elif pos == Tile.CORNER:
          tile = CornerTile(up=up,right=right,down=down,left=left,tile_type=pos)
        else:
          tile = Tile(up=up,right=right,down=down,left=left,tile_type=Tile.CENTRAL)
        tiles.append(tile)

      self.N = int(sqrt(len(tiles)))
      self.max_score = 2*self.N*(self.N-1)
      self.best.arrange(tiles)
      self.set_chances()

    self.current = deepcopy(self.best)
    self.k_max = self.N / 2

    with open('initial.txt','w') as f:
      for l in self.current.board_matrix:
        for el in l:
          u,r,d,l = el.tile.pieces
          outstring = '{} {} {} {}\n'.format(u,r,d,l)
          f.writelines(outstring)



  def set_chances(self):
    curr_tot = 0.0
    self.chances[Tile.CENTRAL] = 0.0
    for i in range(1,self.k+1,1):
      j = self.N -2*i
      self.chances[Tile.CENTRAL] += 2*j + 2*(j-2)

    if self.k == self.k_max and self.N % 2 == 1:
      self.chances[Tile.CENTRAL] += 1

    self.chances[Tile.BORDER] = 4.0*(self.N-2)
    self.chances[Tile.CORNER] = 4.0

    for k,v in self.chances.items():
      curr_tot += v
    for k,v in self.chances.items():
      self.chances[k] = self.chances[k]/curr_tot



  def compute(self):
    current = self.best
    cnt = 0
    while (self.k == self.k_max or cnt < 5000) and self.best.evaluate_score() < 40:
      self.generate_neighboor(current)
      local = self.local_search.search(current)
      if local.evaluate_score() > current.evaluate_score():
        current = deepcopy(local)
        self.k = 1
      else:
        if self.k < self.k_max:
          self.k = self.k + 1

      self.set_chances()
      if current.evaluate_score() > self.best.evaluate_score():
        self.best = deepcopy(current)
        print 'best: {}  '.format(self.best.evaluate_score())
      cnt+=1


  def generate_neighboor(self,board):
    tile_list = self.generate_random_tile_type(board)
    tile1 = self.generate_random_tile(tile_list)
    tile2 = self.generate_random_tile(tile_list)
    board.swap(tile1,tile2)


  def generate_random_tile_type(self,board):
    rnd = random.randint(0, 2)
    t_chance = self.prob_map[rnd]/self.total
    while t_chance > self.chances.get(rnd):
      rnd = random.randint(0, 2)
      t_chance = self.prob_map[rnd]/self.total

    t = self.prob_map.get(rnd,None)
    if t is not None:
      self.prob_map[rnd] += 1
    self.total += 1

    return board.tiles[rnd]


  def generate_random_tile(self,tiles_list):
    rnd = random.choice(tiles_list)
    while not self.isinneghiborhood(self.k,rnd.row,rnd.col):
      rnd = random.choice(tiles_list)
    return rnd

  def isinneghiborhood(self,k,i,j):
    expr = ( (i < k or i >= self.current.N-1-k) and 0 <= j <= self.current.N-1 ) or \
           ( (j < k or j >= self.current.N-1-k) and 0 <= i <= self.current.N-1 )
    return expr


  def print_exit_file(self):
    with open('end.txt','w') as f:
      for l in self.best.board_matrix:
        for el in l:
          u,r,d,l = el.tile.pieces
          outstring = '{} {} {} {}\n'.format(u,r,d,l)
          f.writelines(outstring)




if __name__ == "__main__":
  v = VNS()
  v.load_game_file('../game_files/e2_5x5.txt')
  v.compute()
  v.print_exit_file()
  print 'prob'
  print '\n'*2
  print 'centrals :{}'.format(v.prob_map[Tile.CENTRAL]/v.total)
  print 'borders :{}'.format(v.prob_map[Tile.BORDER]/v.total)
  print 'corners :{}'.format(v.prob_map[Tile.CORNER]/v.total)
  print '\n'*2











