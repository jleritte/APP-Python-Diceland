import colors as c
import pygame as pg
from pygame.locals import SRCALPHA, RESIZABLE
from hex_tile import hex_width, hex_height, hex_size, hex_corner
from hex_tile import hex_to_pixel, pixel_to_hex

stp_size = (hex_width+4, hex_height+4)
stp_center = (stp_size[0]/2,stp_size[1]/2)
corners = [hex_corner(stp_center, i) for i in range(6)]
corners_small = [hex_corner(stp_center, i, hex_size*0.2) for i in range(6)]
screen = None
hex_stamp = pg.Surface(stp_size, SRCALPHA)
clock = pg.time.Clock()
Δ_time = int((1/60)*1000)
terrain_colors = {"plains": c.DARKOLIVEGREEN,
          "forest": c.DARKGREEN,
          "towns": c.DIMGREY,
          "hills": c.FIREBRICK,
          "mounts": c.DARKCYAN}
handlers = {}
animations = []


class gui:
  def __init__(slf):
    global screen
    pg.init()
    screen = pg.display.set_mode((800, 800), flags=RESIZABLE)
    pg.display.set_caption("Diceland")

  def update(slf, data):
    time = clock.tick()
    for event in pg.event.get():
      slf.__emit(pg.event.event_name(event.type), event)
    if time <= Δ_time:
      slf.__draw(Δ_time, data)

  def listen(slf, event, handler):
    handlers.update({event: handler})

  def size(slf):
    return screen.get_size()

  def __emit(slf, event, *rest):
    for name, cb in handlers.items():
      if event == name:
        cb(*rest)

  def __draw(slf, ms, data):
    slf.offset = data.offset
    slf.__draw_background(data.valid)
    slf.__draw_map(ms, data.hex_map, data.selected)
    # slf.__draw_hud(data.terrain_tiles, data.selected_terrain)
    for animation in animations:
      slf.__animate(animation, ms)
    pg.display.update()

  def __draw_background(slf, valid):
    x, y = [lngth+hex_size for lngth in screen.get_size()]
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
      draw_hex(hex_to_pixel(h), off=slf.offset)
    for v in valid.values():
      draw_hex(v, bc=c.BLUE, off=slf.offset)

  def __draw_map(slf, ms, hex_map, selected):
    for pos, ci in hex_map.values():
      draw_hex(hex_to_pixel(pos), color=ci, off=slf.offset)

  def __draw_hud(slf, terrain_tiles, selected):
    r, g, b = c.WHITE
    highlight = (r, g, b, 60)
    bc = c.LIGHTGREY
    y = 5
    draw_box(pos=(5, y), size=(160, 160))
    y = 11
    for k, v in terrain_tiles.items():
      center = (120+hex_size/2, y+hex_size/5-3)
      tc = c.WHITE if k == selected else c.BLACK
      draw_text(f"{k}", tc, 20, (11, y))
      draw_text(f"{v}".rjust(2, ' '), tc, 20, (109, y))
      draw_hex(center, color=terrain_colors[k], small=1)
      if k == selected:
        draw_hex(center, color=highlight, bc=bc, small=1)
      y = y + 32

  def add_animation(slf, animation):
    animations.append(animation)

  def __remove_animation(slf, animation):
    anim_index = animations.index(animation)
    del animations[anim_index]

  def __animate(slf, animation, ms):
    animation.step(ms, off=slf.offset)
    if animation.finished():
      slf.__remove_animation(animation)


def draw_box(pos=(0, 0), size=(0, 0), color=c.GREY, border=c.BLACK):
  x, y = pos
  w, h = size
  rect = pg.Rect(x, y, w, h)
  pg.draw.rect(screen, color, rect)
  pg.draw.rect(screen, border, rect, 2)


def draw_text(text="", color=c.BLACK, size=32, pos=(0, 0)):
  font = pg.font.Font('freesansbold.ttf', size)
  font = font.render(text, True, color)
  screen.blit(font, pos)


def draw_hex(pos=(0, 0), color=c.GREY, bc=c.BLACK, small=0, off=(0, 0)):
  hex_stamp.fill((0, 0, 0, 0))
  x, y = pos
  ox, oy = off
  pos = (x-ox-stp_size[0]/2, y-oy-stp_size[1]/2)
  hex_corners = corners if not small else corners_small
  pg.draw.polygon(hex_stamp, color, hex_corners)
  pg.draw.polygon(hex_stamp, bc, hex_corners, 2)
  screen.blit(hex_stamp, pos)
