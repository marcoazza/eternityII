class Color:
  _color_map = {
    0 : 'grey',
    1 : 'yellow',
    2 : 'red',
    3 : 'green',
    4 : 'orange red',
    5 : 'magenta',
    6 : 'blue',
    7 : 'cyan',
    8 : 'firebrick',
    9 : 'plum',
    10 : 'goldenrod',
    11 : 'orchid',
    12 : 'black',
    13 : 'dark green',
    14 : 'chocolate',
    15 : 'snow',
    16 : 'purple',
    17 : 'gold',
    18 : 'coral',
    19 : 'green yellow',
    20 : 'sky blue',
    21 : 'violet red',
    22 : 'lime green',
    23 : 'sandy brown',
    }

  @classmethod
  def color(cls,col='white'):
      return Color._color_map.get(col,'white')
