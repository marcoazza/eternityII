import unittest
from ..vns.board import Board
from ..vns.tile import Tile

from math import sqrt


class TestBoard(unittest.TestCase):
  def setUp(self):
    self.test_board_file = 'eternityii_project/tests/test_file5x5.txt'
    self.board = Board()
    self.test_board = self.board.load_game_file(self.test_board_file)
    self.board.arrange(self.test_board)


  def test_arrange(self):
    N = sqrt(len(self.test_board))
    self.assertEqual(self.board.N, N)
    self.assertEqual(len(self.board.tiles_list), len(self.test_board))
    self.assertEqual(len(self.board.tiles[Tile.CENTRAL]), N**2 - (4 + 4*(N -2)) )
    self.assertEqual(len(self.board.tiles[Tile.CORNER]), 4)
    self.assertEqual(len(self.board.tiles[Tile.BORDER]), 4*(N-2) )


  def test_swap(self):
    corner1 = self.board.tiles[Tile.CORNER][2]
    corner2 = self.board.tiles[Tile.CORNER][0]

    prev_row1,prev_col1 = corner1.row,corner1.col
    prev_row2,prev_col2 = corner2.row,corner2.col

    self.board.swap(corner1, corner2)
    self.assertEqual(corner1.row,prev_row2)
    self.assertEqual(corner1.col,prev_col2)
    self.assertEqual(corner2.row,prev_row1)
    self.assertEqual(corner2.col,prev_col1)

if __name__ == '__main__':
  unittest.main()
