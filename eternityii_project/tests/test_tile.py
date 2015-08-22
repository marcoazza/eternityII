from __future__ import absolute_import
import unittest
from ..vns.tile import Tile

class TestTile(unittest.TestCase):
  def setUp(self):
    self.central = Tile(up=1,right=2,down=3,left=4)

  def test_rotate(self):
    rotated_tile = Tile(up=4,right=1,down=2,left=3)
    self.central.rotate()
    self.assertEqual(rotated_tile.pieces, self.central.pieces)


if __name__ == '__main__':
  unittest.main()
