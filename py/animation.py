class Animation():
  __progress = 0
  __loop = 0
  __dead = 0
  __reverse = False

  def __init__(slf, time, advance=lambda ms: ms, loop=0, stick=0):
    slf.__time = time
    slf.__next = advance
    slf.__loop = loop
    slf.__stick = stick

  def step(slf, ms, off=(0, 0)):
    percent = slf.__progress / slf.__time
    slf.__next(percent, off)
    slf.__progress = slf.__progress + (ms * (-1 if slf.__reverse else 1))
    slf.__check_loop()

  def finished(slf):
    if slf.__stick and slf.__progress > slf.__time:
      slf.__progress = slf.__time
    return slf.__dead or slf.__progress > slf.__time

  def kill(slf):
    slf.__dead = 1

  def __check_loop(slf):
    if slf.__loop and (slf.__progress > slf.__time or slf.__progress < 0):
      if slf.__loop > 1: return slf.__set_reverse()
      slf.__progress = 0

  def __set_reverse(slf):
      slf.__reverse = not slf.__reverse
      slf.__progress = slf.__time if slf.__reverse else 0
