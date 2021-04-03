from animations import white_hex_blink, grow, shrink, slide_out, slide_in
from animations import directions as dirs
from types import SimpleNamespace as ns
from gui import gui, terrain_colors
# from random import choice
from hex_tile import get_hex_neighbors, pixel_to_hex, hex_to_pixel, tile_hash

# dice_pools = []
state = ns(**{
  "run": True,
  "hex_map": {},
  "valid": {},
  "selected": None,
  "offset": (0, 0),
  "active_player": 0,
  "board_size": 36,
  "terrain_tiles": {
    "plains": 12, "forest": 9, "towns": 6, "hills": 6, "mounts": 3
  },
  "selected_terrain": "plains"
})
ms_st = ns(**{
  "but_1": 0,
  "but_2": 0,
  "last": (0, 0)
})


# # Dice functions
# def generate_dice(count = 6,size = 6):
#     if count < 6:
#         count = 6
#     return {hash(die):die[0] for die in[(roll_die((size,)),x)
#                      for x in range(count)]}

# def roll_die(die = (6,)):
#     return (die[0],choice(range(die[0])) + 1)

# def combine_dice(a = (6,1),b = (6,1)):
#     (s1,p1) = a
#     (s2,p2) = b
#     return (s1, p1 + p2 if p1 + p2 <= s1 else s1)

# def add_die_to_map(hex_tile = (0,0,0),die = (6,1),player = 0):
#     if len(hex_tile) > 2:
#         return False
#     (coords,terrain) = hex_tile
#     hex_map[hex_hash] = (coords,terrain,(player,die))
#     return True

# def get_die_from_map(hex_tile = (0,0)):
#     if len(hex_tile) == 2:
#         return None
#     (coords,terrain,die) = hex_tile
#     return die

# def get_die_from_pool(die_hash,player=0):
#     die = dice_pools[player].get(die_hash,None)
#     return die

# Game State functions
# def set_board_size(num = 8):
#     if num % 2 != 0:
#         num++
#     if num < 8:
#         num = 8
#     board_size = num


def add_hex_to_map(hex_coords=(0, 0), terrain=0):
  hex_hash = tile_hash(hex_coords)
  if not state.hex_map.get(hex_hash, None):
    state.hex_map[hex_hash] = [hex_coords, terrain]
    update_valid(hex_coords)


def update_valid(hex_coords=(0, 0)):
  for n in get_hex_neighbors(hex_coords):
    add_to_valid(n)


def add_to_valid(hex_coords):
  n_hash = tile_hash(hex_coords)
  if not state.hex_map.get(n_hash, None) or not state.valid.get(n_hash, None):
    state.valid[n_hash] = hex_to_pixel(hex_coords)


def click_handler(pos):
  x, y = pos
  if x <= 167 and y <= 167:
    handle_hex_select(y)
  else:
    handle_hex_click(x, y)


def handle_hex_select(y):
  if y <= 31:
    state.selected_terrain = 'plains'
  elif y <= 63:
    state.selected_terrain = 'forest'
  elif y <= 95:
    state.selected_terrain = 'towns'
  elif y <= 127:
    state.selected_terrain = 'hills'
  else:
    state.selected_terrain = 'mounts'


def handle_hex_click(x, y):
  terrain = state.selected_terrain
  ox, oy = state.offset
  coords = pixel_to_hex((x+ox, y+oy))
  hex_hash = tile_hash(coords)
  if state.hex_map.get(hex_hash, None):
    update_selected(hex_hash)
  elif len(state.hex_map) == 0 or state.valid.get(hex_hash, None):
    count = state.terrain_tiles[terrain]
    if count:
      add_hex_to_map(coords, terrain_colors[terrain])
      state.terrain_tiles[terrain] = count - 1
  if len(state.hex_map) == state.board_size:
    state.valid = {}


def update_selected(hex_hash):
  if state.selected is not None:
    state.selected[2].kill()
  p, c = state.hex_map[hex_hash]
  blink = white_hex_blink(state.hex_map[hex_hash])
  state.selected = (p, c, blink)
  ui.add_animation(blink)

# def on_key_press(event):
#   print(dir(event),event.key)


def on_click(pos=(0, 0), button=1):
  if button == 1:
    ms_st.but_1 = 1
    click_handler(pos)
  if button == 3:
    ms_st.but_2 = 1
    ms_st.last = pos


def on_release(pos=(0, 0), button=1):
  if button == 1:
    ms_st.but_1 = 0
  if button == 3:
    ms_st.but_2 = 0


def on_drag(pos=(0, 0)):
  x1, y1 = pos
  x2, y2 = ms_st.last
  ox, oy = state.offset
  state.offset = (ox+(x2-x1), oy+(y2-y1))
  ms_st.last = pos


def end_game(event):
  state.run = False


ui = gui()
def main():
  print('Welcome to Diceland')
  ui.listen("MouseButtonDown", lambda e: on_click(e.pos, e.button))
  ui.listen("MouseButtonUp", lambda e: on_release(e.pos, e.button))
  ui.listen("MouseMotion", lambda e: on_drag(e.pos) if ms_st.but_2 else None)
  ui.listen("Quit", end_game)
  ui.add_animation(white_hex_blink(((6, 1), (0, 0, 0)), 1, 500))
  ui.add_animation(white_hex_blink(((6, 2), (0, 0, 0)), ms=500))
  ui.add_animation(white_hex_blink(((5, 3), (0, 0, 0)), ms=1000))
  ui.add_animation(grow((5, 5), (150, 300)))
  ui.add_animation(shrink((495, 495), (300, 150)))
  ui.add_animation(slide_out((230, 240), (300, 150), dirs.TOP))
  ui.add_animation(slide_out((240, 250), (300, 150), dirs.LEFT))
  ui.add_animation(slide_out((250, 260), (300, 150), dirs.BOTTOM))
  ui.add_animation(slide_out((260, 270), (300, 150), dirs.RIGHT))
  ui.add_animation(slide_in((230, 240), (300, 150), dirs.TOP))
  ui.add_animation(slide_in((240, 250), (300, 150), dirs.LEFT))
  ui.add_animation(slide_in((250, 260), (300, 150), dirs.BOTTOM))
  ui.add_animation(slide_in((260, 270), (300, 150), dirs.RIGHT))
  while state.run:
    ui.update(state)


main()
