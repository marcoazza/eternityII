from localsearch import LocalSearch
from copy import deepcopy

class SteepestDescent(LocalSearch):
  def __init__(self):
    self.local_board = None
    self.better = None

  def search(self,board):
    local_board = deepcopy(board)
    while self.explore_neighborhood(local_board):
      local_board = self.better

    return self.better


  def explore_neighborhood(self,current):
    better = False
    mat = current.board_matrix
    for i in range(1,len(mat)-1):
      for j in range(1,len(mat[i])-1):
        for rot in range(4):
          current.rotate(mat[i][j].tile)
          new_score = current.evaluate_score()
          if self.better is None or new_score > self.better.score:
            self.better = current
            better = True
            return better
    return better
