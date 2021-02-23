from random import choice
from math import sqrt,pi,cos,sin
from turtle import *

# dice_pools = []
hex_map = {}
# active_player = 0
# board_size = 0
selected = None

# # Dice functions
# def generate_dice(count = 6,size = 6):
#   if count < 6:
#     count = 6
#   return {hash(die):die[0] for die in[(roll_die((size,)),x) for x in range(count)]}

# def roll_die(die = (6,)):
#   return (die[0],choice(range(die[0])) + 1)

# def combine_dice(a = (6,1),b = (6,1)):
#   (s1,p1) = a
#   (s2,p2) = b
#   return (s1, p1 + p2 if p1 + p2 <= s1 else s1)

# def add_die_to_map(hex_tile = (0,0,0),die = (6,1),player = 0):
#   if len(hex_tile) > 2:
#     return False
#   (coords,terrain) = hex_tile
#   hex_map[hex_hash] = (coords,terrain,(player,die))
#   return True

# def get_die_from_map(hex_tile = (0,0)):
#   if len(hex_tile) == 2:
#     return None
#   (coords,terrain,die) = hex_tile
#   return die

# def get_die_from_pool(die_hash,player=0):
#   die = dice_pools[player].get(die_hash,None)
#   return die


# # Hex functions
neighbors = [(1,0),(1,-1),(0,-1),(-1,0),(-1,1),(0,1)]
scroll = (0,0)
size = 800 / 15
def tile_hash(coords):
  q,r = coords
  x,y = hex_to_pixel(coords)
  return hash((q,-q-r,r,x,y))

def get_neighbors(Hex = (0,0)):
  (q1,r1) = Hex
  return [(q1 + q2,r1 + r2) for (q2,r2) in neighbors]

def pixel_to_hex_coord(point = (0,0)):
  (x,y) = point
  q = (sqrt(3)/3 * x - 1./3 * y) / size
  r = (2./3 * y) / size
  return round_hex_coord((q,r))

def hex_to_pixel(Hex = (0,0)):
    (q,r) = Hex
    x = size * (sqrt(3) * q + sqrt(3)/2 * r)
    y = size * (3./2 * r)
    return (x, y)

def round_hex_coord(Hex = (0,0)):
  (x,z) = Hex
  rx = round(x)
  ry = round(-x-z)
  rz = round(z)

  x_dif = abs(rx - x)
  y_dif = abs(ry - x-z)
  z_dif = abs(rz - z)

  if x_dif > y_dif and x_dif > z_dif:
    rx = -ry-rz
  elif y_dif > z_dif:
    ry = -rx-rz
  else:
    rz = -rx-ry

  return (rx,rz)

def add_hex_to_map(hex_coords = (0,0),terrain = 0):
  x,z = hex_coords
  hex_hash = tile_hash(hex_coords)
  if not hex_map.get(hex_hash,None):
    hex_map[hex_hash] = (hex_coords,terrain)
    return True
  return False

def select_hex_tile(x,y):
  global selected
  hex_coords = pixel_to_hex_coord((x,y))
  hex_tile = hex_map.get(tile_hash(hex_coords),None)
  if hex_tile:
    selected = hex_tile
    draw_map()


# # Game State functions
# def set_board_size(num = 8):
#   if num % 2 != 0:
#     num++
#   if num < 8:
#     num = 8
#   board_size = num

wn = Screen()
wn.title("Diceland")
wn.setup(width=800,height=800)
wn.tracer(0)

def create_hex_shape():
  corners = [flat_hex_corner(x) for x in range(6)]
  wn.register_shape("hexagon",tuple(corners))

def flat_hex_corner(i):
  angle_deg = 60 * i
  angle_rad = pi / 180 * angle_deg
  return (size * cos(angle_rad),size * sin(angle_rad))

outcolors = ['black','white','blue','purple1']
colors = ['gray30','dark olive green','dark green','dim grey','firebrick','dark cyan','olive','forest green','light grey','red','cyan']

def add_hexagon(pos = (0,0),ci = 0,out = 0):
  (x,y) = hex_to_pixel(pos)
  temp = Turtle()
  temp.speed(0)
  temp.shape("hexagon")
  temp.penup()
  temp.goto(x,y)
  temp.shapesize(outline=2)
  temp.onclick(select_hex_tile)
  temp.color(outcolors[out],colors[ci])

def draw_map():
  for pos,ci in hex_map.values():
    add_hexagon(pos,ci)

  if selected:
    pos, ci = selected
    for n in get_neighbors(pos):
      th = tile_hash(n)
      tile = hex_map.get(th,None)
      if tile:
        add_hexagon(n,tile[1],out=3)
    add_hexagon(pos,ci+5,1)
  wn.update()

ci = [36,24,15,9,3]
def click_handler(x,y):
  for i in ci:
    color = ci.index(i) if len(hex_map) < i else color
  coords = pixel_to_hex_coord((x,y))
  add_hex_to_map(coords,color+1)
  for n in get_neighbors(coords):
    add_hexagon(n,out=2)
  if len(hex_map) > 35:
    wn.onclick(None)
    fill_empty_map()
  draw_map()

def fill_empty_map():
  grid = []
  x = 400
  y = 400
  while x > 0:
    while y > 0:
      grid.append(pixel_to_hex_coord((x,y)))
      grid.append(pixel_to_hex_coord((x,-y)))
      grid.append(pixel_to_hex_coord((-x,-y)))
      grid.append(pixel_to_hex_coord((-x,y)))
      y = y - 45
    y = 400
    x = x - 45
  for h in grid:
    add_hexagon(pos = h)
  wn.update()

wn.onclick(click_handler)
create_hex_shape()
fill_empty_map()

print(f'Welcome to Diceland')


# while True:
#   wn.update()
wn.mainloop()