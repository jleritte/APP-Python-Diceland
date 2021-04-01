import colors as c
from hex_tile import hex_to_pixel, get_hex_neighbors, tile_hash
from gui import draw_box, draw_hex, draw_text

class Animation():
  __progress = 0
  __loop = 0
  __dead = 0

  def __init__(slf, time, advance=lambda ms: ms, loop=0):
    slf.__time = time
    slf.__next = advance
    slf.__loop = loop

  def step(slf, ms, off=(0, 0)):
    percent = slf.__progress / slf.__time
    slf.__next(percent, off)
    slf.__progress += ms
    if slf.__loop and slf.__progress > slf.__time:
      # slf.__progress = 0
      slf.__progress = slf.__time

  def finished(slf):
    return slf.__progress > slf.__time or slf.__dead

  def kill(slf):
    slf.__dead = 1


def white_hex_blink(selected, hex_map):
  hex_blink_step = 40
  blink_dir = 0.75

  def step(ms, off=(0, 0)):
    nonlocal hex_blink_step, blink_dir
    r, g, b = c.WHITE
    pos, ci = selected
    for n in get_hex_neighbors(pos):
      tile = hex_map.get(tile_hash(n), None)
      if tile:
        p, ci = tile
        coords = hex_to_pixel(p)
        bc = c.PURPLE
        draw_hex(coords, color=ci, bc=bc, off=off)
    coords = hex_to_pixel(pos)
    highlight = (r, g, b, hex_blink_step)
    bc = c.YELLOW
    draw_hex(coords, color=highlight, bc=bc, off=off)
    if hex_blink_step > 180 or hex_blink_step < 40:
      blink_dir *= -1
    hex_blink_step += ms * blink_dir

  return step


def slide_in(pos=(0, 0), size=(0, 0), drtn=0, ss=(50, 50)):
  x1, y1 = [(0 - l) if drtn < 2 else (sl + l) for l,sl in zip(size,ss)]
  Δx, Δy = [(a - b) for a, b in zip(pos,(x1, y1))]
  x2, y2 = pos
  vert = drtn % 2 == 0

  def step(percent, off=(0, 0)):
    x = (x1 + Δx * percent) if not vert else x2
    y = (y1 + Δy * percent) if vert else y2
    draw_box((x, y), size)

  return step


def slide_out(pos=(0, 0), size=(0, 0), drtn=0, ss=(50, 50)):
  end = [(0 - l) if drtn < 2 else (sl + l) for l,sl in zip(size,ss)]
  Δx, Δy = [(b - a) for a, b in zip(pos,end)]
  x2, y2 = pos
  vert = drtn % 2 == 0

  def step(percent, off=(0, 0)):
    x = (x2 + Δx * percent) if not vert else x2
    y = (y2 + Δy * percent) if vert else y2
    draw_box((x, y), size)

  return step


def grow(pos=(0, 0), size=(0, 0)):
  start = [(p + p + s) / 2 for p, s in zip(pos, size)]
  Δ = [a - b for a, b in zip(start, pos)]

  def step(percent, off=(0, 0)):
    x, y = [a - b * percent for a, b in zip(start, Δ)]
    w, h = [(l * percent) for l in size]
    draw_box((x, y), (w, h))

  return step


def shrink(pos=(0, 0), size=(0, 0)):
  start = [(p + p + s) / 2 for p, s in zip(pos, size)]
  Δ = [a - b for a, b in zip(start, pos)]

  def step(percent, off=(0, 0)):
    x, y = [a + b * percent for a, b in zip(pos, Δ)]
    w, h = [(l * (1 - percent)) for l in size]
    draw_box((x, y), (w, h))

  return step


def modal(text="hello"):
  draw_text(text)