import pygame as pg
from pygame.locals import SRCALPHA, RESIZABLE
from colors import c_DARKOLIVEGREEN, c_DARKGREEN, c_FIREBRICK, c_DARKCYAN
from colors import c_DIMGREY, c_GREY, c_LIGHTGREY
from colors import c_BLACK, c_WHITE, c_BLUE, c_PURPLE, c_YELLOW
from hex_tile import hex_width, hex_height, hex_size, hex_corner
from hex_tile import hex_to_pixel, pixel_to_hex, get_hex_neighbors, tile_hash

stp_size = (hex_width+4, hex_height+4)
stp_center = (stp_size[0]/2,stp_size[1]/2)
corners = [hex_corner(stp_center, i) for i in range(6)]
corners_small = [hex_corner(stp_center, i, hex_size*0.2) for i in range(6)]
hex_stamp = pg.Surface(stp_size, SRCALPHA)
clock = pg.time.Clock()
Δ_time = int((1/60)*1000)
terrain_colors = {"plains": c_DARKOLIVEGREEN,
          "forest": c_DARKGREEN,
          "towns": c_DIMGREY,
          "hills": c_FIREBRICK,
          "mounts": c_DARKCYAN}
handlers = {}


class gui:
  __screen = None
  __hex_blink_step = 40
  __blink_dir = 0.75

  def __init__(slf):
    pg.init()
    slf.__screen = pg.display.set_mode((800, 800), flags=RESIZABLE)
    pg.display.set_caption("Diceland")

  def update(slf, data):
    time = clock.tick()
    for event in pg.event.get():
      slf.__emit(pg.event.event_name(event.type), event)
    if time <= Δ_time:
      slf.__draw(Δ_time, data)

  def listen(slf, event, handler):
    handlers.update({event: handler})

  def __emit(slf, event, *rest):
    for name, cb in handlers.items():
      if event == name:
        cb(*rest)

  def __draw(slf, ms, data):
    slf.offset = data.offset
    slf.__draw_background(data.valid)
    slf.__draw_map(ms, data.hex_map, data.selected)
    slf.__draw_hud(data.terrain_tiles, data.selected_terrain)
    pg.display.update()

  def __draw_background(slf, valid):
    x, y = [lngth+hex_size for lngth in slf.__screen.get_size()]
    ox, oy = slf.offset
    grid = []
    y_reset = y
    while x > -hex_size:
      while y > -hex_size:
        grid.append(pixel_to_hex((x+ox, y+oy)))
        y = y - hex_size
      y = y_reset
      x = x - hex_size
    for h in grid:
      slf.__draw_hex(hex_to_pixel(h))
    for v in valid.values():
      slf.__draw_hex(v, bc=c_BLUE)

  def __draw_map(slf, ms, hex_map, selected):
    for pos, ci in hex_map.values():
      slf.__draw_hex(hex_to_pixel(pos), color=ci)

    if selected:
      r, g, b = c_WHITE
      pos, ci = selected
      highlight = (r, g, b, slf.__hex_blink_step)
      for n in get_hex_neighbors(pos):
        tile = hex_map.get(tile_hash(n), None)
        if tile:
          p, ci = tile
          coords = hex_to_pixel(p)
          bc = c_PURPLE
          slf.__draw_hex(coords, color=ci, bc=bc)
      coords = hex_to_pixel(pos)
      bc = c_YELLOW
      slf.__draw_hex(coords, color=highlight, bc=bc)
      if slf.__hex_blink_step > 180 or slf.__hex_blink_step < 40:
        slf.__blink_dir *= -1
      slf.__hex_blink_step += ms * slf.__blink_dir

  def __draw_hud(slf, terrain_tiles, selected):
    r, g, b = c_WHITE
    highlight = (r, g, b, 60)
    bc = c_LIGHTGREY
    y = 5
    slf.__draw_box(pos=(5, y), size=(160, 160))
    y = 11
    for k, v in terrain_tiles.items():
      center = (120+hex_size/2, y+hex_size/5-3)
      tc = c_WHITE if k == selected else c_BLACK
      slf.__draw_text(f"{k}", tc, 20, (11, y))
      slf.__draw_text(f"{v}".rjust(2, ' '), tc, 20, (109, y))
      slf.__draw_hex(center, color=terrain_colors[k], small=1)
      if k == selected:
        slf.__draw_hex(center, color=highlight, bc=bc, small=1)
      y = y + 32

  def __draw_box(slf, pos=(0, 0), size=(0, 0), color=c_GREY, border=c_BLACK):
    x, y = pos
    w, h = size
    rect = pg.Rect(x, y, w, h)
    pg.draw.rect(slf.__screen, color, rect)
    pg.draw.rect(slf.__screen, border, rect, 2)

  def __draw_text(slf, text="", color=c_BLACK, size=32, pos=(0, 0)):
    font = pg.font.Font('freesansbold.ttf', size)
    font = font.render(text, True, color)
    slf.__screen.blit(font, pos)

  def __draw_hex(slf, pos=(0, 0), color=c_GREY, bc=c_BLACK, small=0):
    hex_stamp.fill((0, 0, 0, 0))
    x, y = pos
    ox, oy = slf.offset
    if small:
      ox = oy = 0
    pos = (x-ox-stp_size[0]/2, y-oy-stp_size[1]/2)
    hex_corners = corners if not small else corners_small
    pg.draw.polygon(hex_stamp, color, hex_corners)
    pg.draw.polygon(hex_stamp, bc, hex_corners, 2)
    slf.__screen.blit(hex_stamp, pos)
