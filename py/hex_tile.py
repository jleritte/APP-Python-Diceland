from math import sqrt,pi,cos,sin

neighbors = [(1,0),(1,-1),(0,-1),(-1,0),(-1,1),(0,1)]
hex_size = 800 / 14
hex_height = round(hex_size*2)
hex_width = round(3**(1/2)*hex_size)
def tile_hash(coords = (0,0)):
  q,r = coords
  x,y = hex_to_pixel(coords)
  return hash((q,-q-r,r,x,y))

def get_hex_neighbors(Hex = (0,0)):
  (q1,r1) = Hex
  return [(q1 + q2,r1 + r2) for (q2,r2) in neighbors]

def pixel_to_hex(point = (0,0)):
  x,y = point
  q = (sqrt(3)/3 * x - 1./3 * y) / hex_size
  r = (2./3 * y) / hex_size
  return round_hex_coord((q,r))

def hex_to_pixel(Hex = (0,0)):
    q,r = Hex
    x = hex_size * (sqrt(3) * q + sqrt(3)/2 * r)
    y = hex_size * (3./2 * r)
    return (x, y)

def round_hex_coord(Hex = (0,0)):
  (x,z) = Hex
  rx = round(x)
  ry = round(-x-z)
  rz = round(z)

  x_dif = abs(rx - x)
  y_dif = abs(ry - x-z)
  z_dif = abs(rz - z)

  if x_dif > y_dif and x_dif > z_dif:
    rx = -ry-rz
  elif y_dif > z_dif:
    ry = -rx-rz
  else:
    rz = -rx-ry

  return (rx,rz)
def hex_corner(center,i,size=hex_size):
  x,y = center
  angle_deg = 60 * i -30
  angle_rad = pi / 180 * angle_deg
  return (round(x + size * cos(angle_rad)),round(y + size * sin(angle_rad)))