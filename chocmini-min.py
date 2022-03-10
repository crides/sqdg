from sqdg import col, thumb_col, export_color

chocmin_x, chocmin_y, chocmin_nnx = 18, 13.5, 14.5
chocmin_nx = (chocmin_x + chocmin_nnx) / 2
chocmin_off = chocmin_nx / 2 - (chocmin_nx - chocmin_x / 2)
gap = 0.75
params = {"gap": gap, "cr": 75, "sh": 2.5, "ang": 35}

F = col(chocmin_x, chocmin_y, **params)
R = col(chocmin_nx, chocmin_y, off=-chocmin_off, **params)
L = col(chocmin_nx, chocmin_y, off=chocmin_off, **params)
N = col(chocmin_nnx, chocmin_y, **params)
T = thumb_col(chocmin_x, chocmin_y, h=1.5, ang=15, gap=gap)

right = T | L | R | F | L | N
left = T | L | R | F | R | N
whole = left + right

if "show_object" in locals():
    show_object(whole.thing, "whole")

export_color(whole, "whole")
