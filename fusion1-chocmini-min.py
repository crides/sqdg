from sqdg import Config, col, thumb_col, export_color

chocmin_x, chocmin_y, chocmin_nnx = 18, 13.5, 14.5
chocmin_nx = (chocmin_x + chocmin_nnx) / 2
chocmin_off = chocmin_nx / 2 - (chocmin_nx - chocmin_x / 2)
c = Config(gap=0.75, cr=75, sh=3.5, ang=35)

F = col(c + Config(chocmin_x, chocmin_y))
R = col(c + Config(chocmin_nx, chocmin_y, off=-chocmin_off, crh=85))
RI = col(c + Config(chocmin_nnx, chocmin_y, off=chocmin_nnx, crh=85, soff=0))
L = col(c + Config(chocmin_nx, chocmin_y, off=chocmin_off, crh=85))
LI = col(c + Config(chocmin_nnx, chocmin_y, off=-chocmin_nnx, crh=85, soff=0))
N = col(c + Config(chocmin_nnx, chocmin_y))
T = thumb_col(c + Config(chocmin_x, chocmin_y, eh=1.5, ang=15))

right = T | RI | R | F | L | N
left = T | N | R | F | L | LI
whole = left + right

if "show_object" in locals():
    show_object(whole.thing, "whole")

export_color(whole.thing, "fusion1-chocmini-min-whole")
