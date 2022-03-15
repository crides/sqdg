from sqdg import Config,col, thumb_col, export_color

chocmin_x, chocmin_y, chocmin_nnx = 18, 15, 15
chocmin_nx = (chocmin_x + chocmin_nnx) / 2
chocmin_off = chocmin_nx / 2 - (chocmin_nx - chocmin_x / 2)
gap = 0.5
c = Config(gap=gap, ch=1, cr=45, ang=30, eh=1.2, r=53)

F = col(c + Config(chocmin_x, chocmin_y))
R = col(c + Config(chocmin_nx, chocmin_y, off=-chocmin_off))
L = col(c + Config(chocmin_nx, chocmin_y, off=chocmin_off))
N = col(c + Config(chocmin_nnx, chocmin_y))
T = thumb_col(c + Config(chocmin_x, chocmin_y, eh=1.5, ang=15))

right = T | L | R | F | L | N
left = T | L | R | F | R | N
whole = left + right

if "show_object" in locals():
    show_object(whole.thing, "whole")

export_color(whole, "chocmin-whole")
