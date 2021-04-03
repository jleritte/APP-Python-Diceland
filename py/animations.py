import colors as c
from types import SimpleNamespace as ns
from animation import Animation as anim
from hex_tile import hex_to_pixel
from gui import draw_box, draw_hex, draw_text, screen

directions = ns(**{
  "TOP":0,
  "LEFT":1,
  "BOTTOM":3,
  "RIGHT":4
})


def white_hex_blink(selected, loop=2, ms=200):
  def step(percent, off=(0, 0)):
    r, g, b = c.WHITE
    pos, ci = selected
    coords = hex_to_pixel(pos)
    highlight = (r, g, b, 255 * percent)
    bc = c.YELLOW
    draw_hex(coords, color=highlight, bc=bc, off=off)

  return anim(ms, step, loop)


def slide_in(pos, size, drtn, ms=1000):
  ss = screen.get_size()
  x1, y1 = [(0 - l) if drtn < 2 else (sl + l) for l,sl in zip(size,ss)]
  Δx, Δy = [(a - b) for a, b in zip(pos,(x1, y1))]
  x2, y2 = pos
  vert = drtn % 2 == 0

  def step(percent, off=(0, 0)):
    x = (x1 + Δx * percent) if not vert else x2
    y = (y1 + Δy * percent) if vert else y2
    draw_box((x, y), size)

  return anim(ms, step, stick=1)


def slide_out(pos, size, drtn, ms=1000):
  ss = screen.get_size()
  end = [(0 - l) if drtn < 2 else (sl + l) for l,sl in zip(size,ss)]
  Δx, Δy = [(b - a) for a, b in zip(pos,end)]
  x2, y2 = pos
  vert = drtn % 2 == 0

  def step(percent, off=(0, 0)):
    x = (x2 + Δx * percent) if not vert else x2
    y = (y2 + Δy * percent) if vert else y2
    draw_box((x, y), size)

  return anim(ms, step)


def grow(pos, size, ms=1000):
  start = [(p + p + s) / 2 for p, s in zip(pos, size)]
  Δ = [a - b for a, b in zip(start, pos)]

  def step(percent, off=(0, 0)):
    x, y = [a - b * percent for a, b in zip(start, Δ)]
    w, h = [(l * percent) for l in size]
    draw_box((x, y), (w, h))

  return anim(ms, step, stick=1)


def shrink(pos, size, ms=1000):
  start = [(p + p + s) / 2 for p, s in zip(pos, size)]
  Δ = [a - b for a, b in zip(start, pos)]

  def step(percent, off=(0, 0)):
    x, y = [a + b * percent for a, b in zip(pos, Δ)]
    w, h = [(l * (1 - percent)) for l in size]
    draw_box((x, y), (w, h))

  return anim(ms, step)


def modal(text="hello"):
  draw_text(text)