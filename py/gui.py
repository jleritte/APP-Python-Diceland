import pygame as pg
from pygame.locals import *
from colors import *
from hex_tile import hex_width,hex_height,hex_size,hex_corner,hex_to_pixel,pixel_to_hex,get_hex_neighbors,tile_hash

stamp_size = (hex_width+4,hex_height+4)
corners = [hex_corner((stamp_size[0]/2,stamp_size[1]/2),i) for i in range(6)]
corners_small = [hex_corner((stamp_size[0]/2,stamp_size[1]/2),i,hex_size*0.2) for i in range(6)]
hex_stamp = pg.Surface(stamp_size,SRCALPHA)
clock = pg.time.Clock()
Δ_time = int((1/60)*1000)
terrain_colors = {"plains":c_DARKOLIVEGREEN,"forest":c_DARKGREEN,"towns":c_DIMGREY,"hills":c_FIREBRICK,"mounts":c_DARKCYAN}
handlers = []

class gui:
  __screen = None
  __hex_blink_step = 40
  __blink_dir = 0.75
  def __init__(self):
    pg.init()
    self.__screen = pg.display.set_mode((800,800),flags=RESIZABLE)
    pg.display.set_caption("Diceland")

  def update(self,data):
    time = clock.tick()
    for event in pg.event.get():
      self.__emit(pg.event.event_name(event.type),event)
    if time <= Δ_time:
      self.__draw(Δ_time,data)

  def listen(self,event,handler):
    handlers.append((event,handler))

  def __emit(self,event,*rest):
    for name,cb in handlers:
      if event == name:
        cb(*rest)

  def __draw(self,ms,data):
    self.__draw_background(data.valid,data.offset)
    self.__draw_map(ms,data.hex_map,data.selected,data.offset)
    self.__draw_hud(data.terrain_tiles,data.selected_terrain)
    pg.display.update()

  def __draw_background(self,valid,offset):
    x,y = [l+hex_size for l in self.__screen.get_size()]
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
      self.__draw_hex(hex_to_pixel(h),offset=offset)
    for v in valid.values():
      self.__draw_hex(v,border=c_BLUE,offset=offset)

  def __draw_map(self,ms,hex_map,selected,offset):
    for pos,ci in hex_map.values():
      self.__draw_hex(center=hex_to_pixel(pos),color=ci,offset=offset)

    if selected:
      r,g,b = c_WHITE
      pos,ci = selected
      for n in get_hex_neighbors(pos):
        tile = hex_map.get(tile_hash(n),None)
        if tile:
          p,ci = tile
          self.__draw_hex(center=hex_to_pixel(p),color=ci,border=c_PURPLE,offset=offset)
      self.__draw_hex(center=hex_to_pixel(pos),color=(r,g,b,self.__hex_blink_step),border=c_YELLOW,offset=offset)
      if self.__hex_blink_step > 180 or self.__hex_blink_step < 40:
        self.__blink_dir *= -1
      self.__hex_blink_step += ms * self.__blink_dir

  def __draw_hud(self,terrain_tiles,selected):
    r,g,b = c_WHITE
    y = 5
    self.__draw_box(pos=(5,y),size=(160,160))
    y = 11
    for k,v in terrain_tiles.items():
      self.__screen.blit(self.__draw_text(f"{k}",c_WHITE if k == selected else c_BLACK,20),(11,y))
      self.__screen.blit(self.__draw_text(f"{v}".rjust(2,' '),c_WHITE if k == selected else c_BLACK,20),(109,y))
      self.__draw_hex(center=(120+hex_size/2,y+hex_size/5-3),color=terrain_colors[k],small=1)
      if k == selected:
        self.__draw_hex(center=(120+hex_size/2,y+hex_size/5-3),color=(r,g,b,60),border=c_LIGHTGREY,small=1)
      y = y + 32

  def __draw_box(self,pos=(0,0),size=(0,0),color=c_GREY,border=c_BLACK):
    x,y = pos
    w,h = size
    rect = pg.Rect(x,y,w,h)
    pg.draw.rect(self.__screen,color,rect)
    pg.draw.rect(self.__screen,border,rect,2)

  def __draw_text(self,text="TEST STRING",color=c_BLACK,size=32):
    font = pg.font.Font('freesansbold.ttf',size)
    font = font.render(text,True,color)
    return font

  def __draw_hex(self,center=(0,0),color=c_GREY,border=c_BLACK,small=0,offset=(0,0)):
    hex_stamp.fill((0,0,0,0))
    x,y = center
    ox,oy = offset
    pg.draw.polygon(hex_stamp,color,corners if not small else corners_small)
    pg.draw.polygon(hex_stamp,border,corners if not small else corners_small,2)
    self.__screen.blit(hex_stamp,(x-ox-stamp_size[0]/2,y-oy-stamp_size[1]/2))
