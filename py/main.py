import pygame
from pygame.locals import *
from random import choice
from hex_tile import *
from colors import *

# dice_pools = []
hex_map = {}
# active_player = 0
board_size = 36
selected = None
offset = (0,0)

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

pygame.init()
wn = pygame.display.set_mode((standard_size,standard_size),flags=RESIZABLE)
pygame.display.set_caption("Diceland")

def add_hex_to_map(hex_coords = (0,0),terrain = 0):
  hex_hash = tile_hash(hex_coords)
  if not hex_map.get(hex_hash,None):
    hex_map[hex_hash] = [hex_coords,terrain]
    return True
  return False

stamp_size = (hex_width+4,hex_height+4)
hex_stamp = pygame.Surface(stamp_size,SRCALPHA)
corners = [hex_corner((stamp_size[0]/2,stamp_size[1]/2),i) for i in range(6)]
corners_small = [hex_corner((stamp_size[0]/2,stamp_size[1]/2),i,hex_size*0.2) for i in range(6)]
def draw_hex(center=(0,0),color=c_GREY,border=c_BLACK,small=0):
  hex_stamp.fill((0,0,0,0))
  x,y = center
  ox,oy = offset
  if small:
    ox = 0
    oy = 0
  pygame.draw.polygon(hex_stamp,color,corners if not small else corners_small)
  pygame.draw.polygon(hex_stamp,border,corners if not small else corners_small,2)
  wn.blit(hex_stamp,(x-ox-stamp_size[0]/2,y-oy-stamp_size[1]/2))

def draw_box(pos=(0,0),size=(0,0),color=c_GREY,border=c_BLACK):
  x,y = pos
  w,h = size
  rect = pygame.Rect(x,y,w,h)
  pygame.draw.rect(wn,color,rect)
  pygame.draw.rect(wn,border,rect,2)

def draw_text(text="TEST STRING",color=c_BLACK,size=32):
  font = pygame.font.Font('freesansbold.ttf',size)
  font = font.render(text,True,color)
  return font

def draw(ms):
  draw_background()
  draw_map(ms)
  draw_hud()
  pygame.display.update()

def draw_background():
  x,y = [l+hex_size for l in wn.get_size()]
  ox,oy = offset
  grid = []
  y_reset = y
  while x > -hex_size:
    while y > -hex_size:
      grid.append(pixel_to_hex((x+ox,y+oy)))
      y = y - hex_size
    y = y_reset
    x = x - hex_size
  for h in grid:
    draw_hex(hex_to_pixel(h))

anim_step = 20
anim_dir = 1
steps = 0
def draw_map(ms):
  global anim_step, anim_dir, steps
  for pos,ci in hex_map.values():
    draw_hex(center=hex_to_pixel(pos),color=ci)
    if len(hex_map) < 36:
      for n in get_hex_neighbors(pos):
        tile = hex_map.get(tile_hash(n),None)
        if not tile:
          draw_hex(center=hex_to_pixel(n),border=c_BLUE)

  if selected:
    r,g,b = c_WHITE
    # hightlight = globals().get(f"c_HIGHLIGHT{blink}",(0,0,0,0))
    pos,ci = selected
    for n in get_hex_neighbors(pos):
      tile = hex_map.get(tile_hash(n),None)
      if tile:
        p,ci = tile
        draw_hex(center=hex_to_pixel(p),color=ci,border=c_PURPLE)
    draw_hex(center=hex_to_pixel(pos),color=(r,g,b,anim_step),border=c_WHITE)
    if anim_step > 200 or anim_step < 20:
      print("flip",anim_step,ms,anim_dir,steps)
      anim_dir *= -1
    anim_step += ms * anim_dir
    print(anim_step,anim_dir,ms,steps)
    steps += 1

selected_terrain = 'plains'
terrain_tiles = {"plains": 12,"forest": 9,"towns": 6,"hills": 6,"mounts": 3}
terrain_colors = {"plains":c_DARKOLIVEGREEN,"forest":c_DARKGREEN,"towns":c_DIMGREY,"hills":c_FIREBRICK,"mounts":c_DARKCYAN}
def draw_hud():
  r,g,b = c_WHITE
  y = 5
  draw_box(pos=(5,y),size=(160,160))
  y = 11
  for k,v in terrain_tiles.items():
    wn.blit(draw_text(f"{k}",c_WHITE if k == selected_terrain else c_BLACK,20),(11,y))
    wn.blit(draw_text(f"{v}".rjust(2,' '),c_WHITE if k == selected_terrain else c_BLACK,20),(109,y))
    draw_hex(center=(120+hex_size/2,y+hex_size/5-3),color=terrain_colors[k],small=1)
    if k == selected_terrain:
      draw_hex(center=(120+hex_size/2,y+hex_size/5-3),color=(r,g,b,20),small=1)
    y = y + 32

def click_handler(pos):
  x,y = pos
  if x <= 167 and y <= 167:
    handle_hex_select(x,y)
  else:
    handle_hex_click(x,y)

def handle_hex_select(x,y):
  global selected_terrain
  if y <= 31:
    selected_terrain = 'plains'
  elif y <= 63:
    selected_terrain = 'forest'
  elif y <= 95:
    selected_terrain = 'towns'
  elif y <= 127:
    selected_terrain = 'hills'
  else:
    selected_terrain = 'mounts'

def handle_hex_click(x,y):
  global selected, blink
  ox,oy = offset
  coords = pixel_to_hex((x+ox,y+oy))
  if hex_map.get(tile_hash(coords),None):
    selected = hex_map[tile_hash(coords)]
  elif len(hex_map) < board_size:
    count = terrain_tiles[selected_terrain]
    if count:
      add_hex_to_map(coords,terrain_colors[selected_terrain])
      terrain_tiles[selected_terrain] = count - 1

print(f'Welcome to Diceland')
# print(dir(pygame.locals))
# print(dir(wn))

def handle_key_press(event):
  print(dir(event),event.key)

button_1 = 0
button_2 = 0
def handle_click(pos=(0,0),button=1):
  global button_1,button_2,last
  if button == 1:
    button_1 = 1
    click_handler(pos)
  if button == 3:
    button_2 = 1
    last = pos

def handle_release(pos=(0,0),button=1):
  global button_1,button_2
  if button == 1:
    button_1 = 0
  if button == 3:
    button_2 = 0

last = (0,0)
def handle_drag(pos=(0,0)):
  global last,offset
  x1,y1 = pos
  x2,y2 = last
  ox,oy = offset
  offset = (ox+(x2-x1),oy+(y2-y1))
  last = pos

run = True
clock = pygame.time.Clock()
Δ_time = int((1/60) * 1000)
while run:
  time = clock.tick(60)
  for event in pygame.event.get():
    if event.type == QUIT:
      run = False
    if event.type == KEYDOWN:
      handle_key_press(event)
    if event.type == MOUSEBUTTONDOWN:
      handle_click(event.pos,event.button)
    if event.type == MOUSEBUTTONUP:
      handle_release(event.pos,event.button)
    if event.type == MOUSEMOTION:
      if button_2:
        handle_drag(event.pos)
  draw(Δ_time)