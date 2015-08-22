from board import Board
from tile import Tile
import random
from copy import deepcopy
from steepest_descent import SteepestDescent
import time


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
    tiles = self.current.load_game_file(filename)
    self.current.arrange(tiles)
    self.N = self.current.N
    self.max_score = 2*self.N*(self.N-1)
    self.set_chances()
    self.best = deepcopy(self.current)
    self.k_max = self.N / 2


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



  def compute(self,sec=30):
    print 'compute....'
    current = self.best
    timer = time.time() + sec
    while (self.k == self.k_max or time.time() < timer) and self.best.score < self.max_score:
      self.generate_neighboor(current)
      local = self.local_search.search(current)
      if local.score > current.score:
        current = deepcopy(local)
        self.k = 1
      else:
        if self.k < self.k_max:
          self.k = self.k + 1

      self.set_chances()
      if current.score > self.best.score:
        self.best = deepcopy(current)
        print 'best: {}  '.format(self.best.score)


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
  print 'game file loaded'
  v.compute()

  v.print_exit_file()
