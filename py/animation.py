

class Animation():
  __time = 0
  __loop = 0
  __dead = 0
  def __init__(slf, time, advance=lambda ms: ms, loop=0):
    slf.__time = time
    slf.__next = advance
    slf.__loop = loop
    if loop:
      slf.__reset = time

  def step(slf, ms, off=(0, 0)):
    slf.__time -= ms
    slf.__next(ms, off)
    if slf.__loop and slf.__time <= 0:
      slf.__time = slf.__reset

  def finished(slf):
    return slf.__time <= 0 or slf.__dead

  def kill(slf):
    slf.__dead = 1
