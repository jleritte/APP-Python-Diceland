from random import choice
from turtle import *
from hex_tile import *

# dice_pools = []
hex_map = {}
# active_player = 0
board_size = 36
selected = None
offset = (0,0)
outcolors = ['black','white','blue','purple1']
colors = ['gray30','dark olive green','dark green','dim grey','firebrick','dark cyan','olive','forest green','light grey','red','cyan']

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



# # Game State functions
# def set_board_size(num = 8):
#   if num % 2 != 0:
#     num++
#   if num < 8:
#     num = 8
#   board_size = num

standard_size = 800

wn = Screen()
wn.title("Diceland")
wn.setup(width=standard_size,height=standard_size)
wn.screensize(standard_size/2,standard_size/2)
wn.tracer(0)

wn.register_shape("hexagon",tuple([hex_corner(x) for x in range(6)]))

def add_hex_to_map(hex_coords = (0,0),terrain = 0):
  hex_hash = tile_hash(hex_coords)
  if not hex_map.get(hex_hash,None):
    hex_map[hex_hash] = [hex_coords,terrain]
    return True
  return False

def create_hex():
  temp = Turtle("hexagon")
  temp.speed(0)
  temp.penup()
  temp.shapesize(outline=2)
  temp.ht()
  return temp

def create_box(shape=(1,1,0)):
  w,l,o = shape
  temp = Turtle("square")
  temp.speed(0)
  temp.penup()
  temp.shapesize(w,l,o)
  temp.ht()
  return temp

hex_stamp = create_hex()
def draw():
  hex_stamp.clearstamps()
  hex_stamp.shapesize(1,1,2)
  draw_background()
  draw_map()
  draw_hud()
  wn.update()

def stamp_screen(turt,pos=(0,0),color=(0,0),off=1):
  oi, ci = color
  ox,oy = offset
  x, y = pos
  if off:
    x = x - ox
    y = y - oy
  turt.color(outcolors[oi],colors[ci])
  turt.goto(x,y)
  turt.stamp()

def draw_background():
  x,y = wn.screensize()
  ox,oy = offset
  grid = []
  y_reset = y
  while x > 0:
    while y > 0:
      grid.append(pixel_to_hex((x+ox,y+oy)))
      grid.append(pixel_to_hex((x+ox,-y+oy)))
      grid.append(pixel_to_hex((-x+ox,y+oy)))
      grid.append(pixel_to_hex((-x+ox,-y+oy)))
      y = y - hex_size
    y = y_reset
    x = x - hex_size
  for h in grid:
    x,y = hex_to_pixel(h)
    stamp_screen(hex_stamp,pos=(x,y),color=(0,0))

def draw_map():
  for pos,ci in hex_map.values():
    stamp_screen(hex_stamp,pos=hex_to_pixel(pos),color=(0,ci))
    if len(hex_map) < 36:
      for n in get_hex_neighbors(pos):
        tile = hex_map.get(tile_hash(n),None)
        if not tile:
          stamp_screen(hex_stamp,pos=hex_to_pixel(n),color=(2,0))

  if selected:
    pos,ci = selected
    for n in get_hex_neighbors(pos):
      tile = hex_map.get(tile_hash(n),None)
      if tile:
        p,ci = tile
        stamp_screen(hex_stamp,pos=hex_to_pixel(p),color=(3,ci))
    stamp_screen(hex_stamp,pos=hex_to_pixel(pos),color=(1,ci+5))

selected_terrain = 'plains'
terrain_tiles = {"plains": 12,"forest": 9,"towns": 6,"hills": 6,"mounts": 3}
terrain_colors = ["plains","forest","towns","hills","mounts"]
hud_stamp = create_box(shape=(8,8,2))
def draw_hud():
  y = 315
  stamp_screen(hud_stamp,pos=(-315,y),color=(0,0),off=0)
  y = 365
  ci = 1
  hci = None
  for k,v in terrain_tiles.items():
    hex_stamp.color(outcolors[0])
    if k == selected_terrain:
      hex_stamp.color(outcolors[1])
      hci = ci + 5
    hex_stamp.goto(-390,y)
    hex_stamp.write(f"{k}",align="left",font=("Sans-serif",16,"normal"))
    hex_stamp.goto(-270,y)
    hex_stamp.write(f"{v}",align="right",font=("Sans-serif",16,"normal"))
    hex_stamp.shapesize(0.25,0.25,2)
    stamp_screen(hex_stamp,pos=(-250,y+15),color=(0,hci if hci else ci),off=0)
    y = y - 32
    ci = ci + 1
    hci = None

def click_handler(x,y):
  if x <= -234 and y >= 233:
    handle_hex_select(x,y)
  else:
    handle_hex_click(x,y)
  draw()

def handle_hex_select(x,y):
  global selected_terrain
  if y >= 366:
    selected_terrain = 'plains'
  elif y >= 339:
    selected_terrain = 'forest'
  elif y >= 305:
    selected_terrain = 'towns'
  elif y >= 276:
    selected_terrain = 'hills'
  else:
    selected_terrain = 'mounts'

def handle_hex_click(x,y):
  global selected
  ox,oy = offset
  coords = pixel_to_hex((x+ox,y+oy))
  if hex_map.get(tile_hash(coords),None):
    selected = hex_map[tile_hash(coords)]
  elif len(hex_map) < board_size:
    count = terrain_tiles[selected_terrain]
    if count:
      add_hex_to_map(coords,terrain_colors.index(selected_terrain)+1)
      terrain_tiles[selected_terrain] = count - 1


step = hex_size / 2
def key_handlers(direction):
  dy = step if direction == "Up" or direction == "Down" else 0
  dx = step if direction == "Left" or direction == "Right" else 0
  def funct():
    global offset
    x,y = offset
    x = x + dx if direction == "Left" else x - dx
    y = y - dy if direction == "Up" else y + dy
    offset = (x,y)
    draw()

  return funct

for n in ["Up","Down","Left","Right"]:
  wn.onkeypress(key_handlers(n),n)

wn.onclick(click_handler)
wn.listen()
draw()

print(f'Welcome to Diceland')
# print(dir(wn))

wn.mainloop()